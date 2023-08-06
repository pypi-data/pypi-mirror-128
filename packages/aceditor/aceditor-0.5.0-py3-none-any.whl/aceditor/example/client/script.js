$(document).ready(function(){
    var backup_post = $.post;
    $.post = undefined;
    var api_url = "api.py";
    function download(filename, text) {
        var e = $("<a/>");
        e.attr("href", "data:text/plain;charset=utf-8," + encodeURIComponent(text));
        e.attr("download", filename);
        e.appendTo("body").hide().get(0).click();
        e.remove();
    }
    function open_path(path) {
        path = path || "/";
        last_path = path;
        backup_post(api_url, {"open": path}, function (response) {
            var htmls = "<div class='files'>";
            if (last_path !== "/") {
                var tmp = decodeURIComponent(last_path);
                tmp = tmp.split("/").slice(0, -1).join("/");
                if (tmp === "") {
                    tmp = "/";
                }
                htmls += "<div data-path='"+ encodeURIComponent(tmp).replace(/[!\'()*]/g, escape)+"'>..</div>";
            }
            for(var i=0;i<response.length;i++){
                for(var j=0;j<response[i].length;j++){
                    var tmp = last_path;
                    if (last_path !== "/") {
                        tmp += "/";
                    }
                    tmp += response[i][j];
                    htmls += "<div data-"+(i?"val":"path")+"='"+encodeURIComponent(tmp).replace(/[!'()*]/g, escape)+"'>"+response[i][j].split("/").slice(-1)[0]+"</div>";
                }
            }
            htmls += "</div>";
            $("div#dialog").append(htmls).show();
            $("div#dialog div.files div").mousedown(function (e) {
                e.preventDefault();
                e.stopPropagation();
                if ($(this).data("path")) {
                    $("div#dialog div.close").click();
                    return open_path(decodeURIComponent($(this).data("path")));
                }
                else if ($(this).data("val")) {
                    var hash = "#" + decodeURIComponent($(this).data("val"));
                    if (e.which === 1) {
                        window.location.hash = hash;
                        try {
                            load_file();
                            $("div#dialog div.close").click();
                        } catch (e) {
                            ;
                        }
                        return;
                    }
                    else if (e.which === 3) {
                        window.open("/"+hash);
                        return false;
                    }
                }
            });
        }).fail(function(){
            $("div#dialog div.close").click();
            alert("open file failed.\nplease try again later.");
        });
    }
    function open_file() {
        open_path(last_path);
    }
    function save_file(e, fp) {
        var history_name;
        if (!fp) {
            fp = window.location.hash.slice(1);
            if (editor.session.getValue() === original_text) {
                set_status("File not needed to save.")
                return;
            }
            history_name = prompt("Why do you save this file?\nThis is used for identify history.\nprintable strings only")||"unknown save";
            var matches = [];
            for (var m of history_name.matchAll(/[A-Za-z0-9_]+/g)) {
                matches.push(m[0]);
            }
            history_name = matches.join("_")||"unknown save";
        }
        var content = editor.session.getValue();
        backup_post(api_url, {"save": fp, "content": btoa(encodeURIComponent(content)), "history_name": history_name}, function (response) {
            $("div#statusbar .statustext").html("File loading ...");
            if (typeof response == "string") {
                set_status("File failed to save.\nReason: "+response);
            }
            else {
                original_text = content;
                window.location.hash = "#"+fp;
            }
        }).fail(function(response){
            set_status("File failed to save. Reason: "+response.responseText);
        });
    }
    function save_as_file(e) {
        var fp = prompt("Current file path: '"+window.location.hash.slice(1)+"'\nEnter new file path: (relative/absolute)");
        if (!fp) return;
        if (confirm("Save as file '"+fp+"'?")) {
            return save_file(e, fp);
        }
    }
    function file_history() {
        backup_post(api_url, {"history": window.location.hash.slice(1)}, function (response) {
            if (response.length > 0) {
                for (var i = 0; i < response.length; i++) {
                    response[i] = response[i].split(".");
                }
                var htmls = "<div class='files'>";
                // htmls += "<div>Current version: "+response[0].slice(-2)[0]+"</div><br/>";
                for (var i = 0; i < response.length; i++) {
                    var name = response[i].slice(-2)[0];
                    // if (i+1 < response.length) {
                    //     name = response[i+1].slice(-2)[0];
                    // }
                    // else {
                    //     name = "- Initial Save -"
                    // }
                    htmls += "<div data-version='" + response[i].join(".") + "'>" + response[i].slice(-3)[0] + ": " + name + "</div>";
                }
                htmls += "</div>";
                $("div#dialog").append(htmls).show();
                $("div#dialog div.files div[data-version]").click(function () {
                    var version = $(this).data("version");
                    backup_post(api_url, {"history": window.location.hash.slice(1), "version": version}, function (response) {
                        if (typeof response == "string") {
                            alert("File failed to history.\nReason: " + response + "\n\neditor will reload.");
                        }
                        window.location.reload();
                    }).fail(function (response) {
                        set_status("File failed to history.\nReason: " + response.responseText);
                    })
                });
            }
            else {
                set_status("File has no history.")
            }
        });
    }
    function support_localStorage() {
        // try {
            var _ = "test";
            window.localStorage.setItem(_, _);
            window.localStorage.removeItem(_);
            return true;
        // } catch(e) {
        //     return false;
        // }
    }
    function bm_toggle(_v){
        if (!_v) return;
        var v = encodeURIComponent(_v);
        if (support_localStorage()) {
            if (bm_get().indexOf(v) === -1) {
                var lastid = bm_lastid_get()+1;
                bm_lastid_set(lastid);
                lastid = "bm"+lastid;
                window.localStorage.setItem(lastid, JSON.stringify(v));
            }
            else {
                bm_rm(_v);
                if (bm_get().length === 0) {
                    bm_lastid_set(0);
                }
            }
        }
    }
    function bm_get(){
        if (support_localStorage()) {
            var _ = [];
            for (var i=0; i<window.localStorage.length; i++) {
                if (window.localStorage.key(i) === "lastid") continue;
                _.push(JSON.parse(window.localStorage[window.localStorage.key(i)]));
            }
            _.sort();
            return _;
        }
    }
    function bm_rm(_v){
        var v = encodeURIComponent(_v);
        if (support_localStorage()) {
            for (var i=0; i<window.localStorage.length; i++) {
                if (JSON.parse(window.localStorage[window.localStorage.key(i)]) === v) {
                    window.localStorage.removeItem(window.localStorage.key(i));
                    break;
                }
            }
        }
    }
    function bm_lastid_get(){
        if (support_localStorage()) {
            try{
                return JSON.parse(window.localStorage.getItem("lastid"));
            }
            catch (e) {
                bm_lastid_set(0);
                return 0;
            }
        }
    }
    function bm_lastid_set(lastid){
        if (support_localStorage()) {
            return window.localStorage.setItem("lastid", JSON.stringify(lastid));
        }
    }
    function bm_export(){
        var v = bm_get();
        for (var i=0; i<v.length; i++) {
            v[i] = decodeURIComponent(v[i]);
        }
        download("ace-bookmark.json", JSON.stringify(v));
    }
    function bm_import(){
        var fi = $("<input type='file' style='display: none'/>");
        fi.appendTo("body");
        fi.change(function (){
            var file = fi.get(0).files[0];
            if (!file) return;
            var reader = new FileReader();
            reader.readAsText(file, "UTF-8");
            reader.onload = function (e) {
                fi.remove();
                var v = e.target.result;
                v = JSON.parse(v);
                for (var i=0; i<v.length; i++) {
                    bm_toggle(v[i]);
                }
                $("div#dialog div.close").click();
                bookmark();
            }
        });
        fi.get(0).click();
    }
    function bookmark() {
        var htmls = "<div class='files'>";
        htmls += "<div id='import_bm' data-dummy>Import Bookmark</div>";
        htmls += "<div id='export_bm' data-dummy>Export Bookmark</div>";
        if (window.location.hash.slice(1)) {
            htmls += "<div id='toggle_bm' data-dummy>Toggle Current File<br>( " + $("<p/>").text(window.location.hash.slice(1)).html() + " )</div>";
        }
        var bms = bm_get() || [];
        var prev_dir = "";
        var max_len_f = -1;
        var max_len_d = -1;
        for (var i = 0; i < bms.length; i++) {
            var bm = $("<p/>").text(decodeURIComponent(bms[i])).html().split("/");
            var len_f = bm.slice(-1)[0].length;
            if (len_f > max_len_f) {
                max_len_f = len_f+1;
            }
            var len_d = bm.slice(0, -1).join("/").length;
            if (len_d > max_len_d) {
                max_len_d = len_d;
            }
        }
        if (max_len_d < max_len_f) {
            max_len_d = max_len_f+4;
        }
        if (bms.length > 0) {
            htmls += "<div data-dummy>&nbsp;</div>";
        }
        for (var i = 0; i < bms.length; i++) {
            var bm = $("<p/>").text(decodeURIComponent(bms[i])).html();
            var cur_dir = bm.split("/");
            var name = cur_dir.slice(-1)[0];
            name = ("    /"+name.padEnd(max_len_f, " ")).replace(/ /g, "&nbsp;");
            cur_dir = cur_dir.slice(0, -1).join("/").padEnd(max_len_d, " ").replace(/ /g, "&nbsp;");
            if (prev_dir !== cur_dir) {
                prev_dir = cur_dir;
                htmls += "<div data-dummy>"+cur_dir+"</div>";
            }
            bm = name;
            htmls += "<div data-val='" + bms[i] + "'>" + bm + "</div>";
        }
        htmls += "</div>";
        $("div#dialog").append(htmls).show();
        $("div#toggle_bm").click(function () {
            bm_toggle(window.location.hash.slice(1));
            $("div#dialog div.close").click();
            bookmark();
        });
        $("div#import_bm").click(bm_import);
        $("div#export_bm").click(bm_export);
        $("div#dialog div.files div[data-val]").mousedown(function (e) {
            e.preventDefault();
            e.stopPropagation();
            var hash = "#" + decodeURIComponent($(this).data("val"));
            if (e.which === 1) {
                window.location.hash = hash;
                try {
                    load_file();
                    $("div#dialog div.close").click();
                } catch (e) {
                    ;
                }
                return;
            } else if (e.which === 3) {
                window.open("/" + hash);
                return false;
            }
        });
    }
    function print() {
        require("ace/config").loadModule("ace/ext/static_highlight", function(m) {
            var result = m.renderSync(
                editor.getValue(), editor.session.getMode(), editor.renderer.theme
            );
            document.body.style.display="none";
            var d = document.createElement("div");
            d.innerHTML=result.html;
            document.documentElement.appendChild(d);
            require("ace/lib/dom").importCssString(result.css);

            setTimeout(function() {window.print()}, 10);

            window.addEventListener("focus", function restore() {
               window.removeEventListener("focus", restore, false);
               d.parentNode.removeChild(d);
               document.body.style.display= "";
               editor.resize(true);
            }, false);
        });
    }
    function gotoline() {
        editor.prompt({ $type: "gotoLine" });
    }
    function build_toolbar(){
        var tools = [
            [
                "div",
                {
                    class: "sponsor ace-tomorrow-night-bright",
                    onclick: function () {
                        open("https://ace.c9.io/build/kitchen-sink.html");
                    }
                },
                "ACE"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "openButton",
                    onclick: open_file
                },
                "Open"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "saveButton",
                    onclick: save_file
                },
                "Save"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "saveAsButton",
                    onclick: save_as_file
                },
                "Save As"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "historyButton",
                    onclick: file_history
                },
                "History"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "bookmarkButton",
                    onclick: bookmark
                },
                "Bookmark"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "findButton",
                    onclick: function () {
                        editor.execCommand("find")
                    }
                },
                "Find"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "findButton",
                    onclick: function () {
                        editor.execCommand("replace")
                    }
                },
                "Replace"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "wrapButton",
                    onclick: function () {
                        wrap_setting = !wrap_setting;
                        editor.setOption("wrap", wrap_setting);
                    }
                },
                "Wrap"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "printButton",
                    onclick: print
                },
                "Print"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "downloadButton",
                    onclick: function () {
                        var fn;
                        if (window.location.hash.slice(1)) {
                            fn = window.location.hash.split("/").slice(-1)[0];
                        }
                        else{
                            var q = window.location.search.split("url=");
                            if (q.length === 2) {
                                fn = q.slice(-1)[0].split("/").slice(-1)[0];
                            }
                            else {
                                return;
                            }
                        }
                        download(fn, editor.session.getValue());
                    }
                },
                "Download"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "logsButton",
                    onclick: function () {
                        window.open("./log.log");
                        window.open("./ace.log");
                    }
                },
                "Logs"
            ],
            [
                "div",
                {
                    class: "ace-tomorrow-night-bright",
                    ref: "helpButton",
                    onclick: function () {
                        var kbs = "<div class='files'><table class='ace-tomorrow-night-bright' style='font-size:2vh; border-collapse: collapse;width: 100%;margin: 0 auto'>";
                        var _ = [];
                        for (var key in editor.keyBinding.$defaultHandler.commandKeyBinding) {
                            _.push([key, editor.keyBinding.$defaultHandler.commandKeyBinding[key]]);
                        }
                        _.sort(function(a, b) {
                            a = a[0];
                            b = b[0];
                            return a < b ? -1 : (a > b ? 1 : 0);
                        });
                        for (var i = 0; i < _.length; i++) {
                            var k = _[i][0].replace(/-/g, " ").split(" ");
                            for (var j=0; j<k.length; j++){
                                k[j] = k[j].substr(0, 1).toUpperCase()+k[j].substr(1);
                            }
                            k = k.join(" ");
                            var v = _[i][1];
                            kbs += "<tr><th>"+k+"</th><td>"+v["description"]+"</td></tr>";
                        }
                        kbs += "</table></div>";
                        $("div#dialog").append(kbs).show();
                    }
                },
                "Help"
            ]
        ];
        var toolbar = [
            "div",
            { class: "toolbar" }
        ];
        var url_blacklist_tools = [
            "Open",
            "Save",
            "Save As",
            "History",
            "Bookmark",
        ];
        for (var i=0; i<tools.length; i++) {
            if (window.location.search.split("url=").length === 2) {
                if (url_blacklist_tools.indexOf(tools[i][2]) !== -1) {
                    continue;
                }
            }
            toolbar.push(tools[i]);
        }
        var buildDom = ace.require("ace/lib/dom").buildDom;
        buildDom(
            toolbar,
            $("div#toolbar").get(0),
            btns
        )
    }
    function set_status(str) {
        var _statusbar = $("div#statusbar .statustext");
        if (_statusbar.html().indexOf(str) !== -1) {
            return;
        }
        if (_statusbar.hasClass("alert")) {
            clearTimeout(statusbarto);
        }
        if (str.indexOf("failed") === -1 && _statusbar.html().indexOf("failed") !== -1) {
            str += " "+_statusbar.html();
        }
        _statusbar.html(str);
        if (str.indexOf("failed") !== -1) {
            _statusbar.addClass("alert");
        }
        if (_statusbar.hasClass("alert")) {
            statusbarto = setTimeout(function () {
                _statusbar.removeClass("alert");
            }, 500);
        }
    }
    function build_cmds(cmd) {
        var [name, description, exec, win, mac, scrollIntoView, multiSelectAction, readOnly] = cmd;
        cmd = {
            "name": name,
            "description": description,
            "exec": exec,
            "bindKey": {}
        };
        if (win) {
            cmd["bindKey"]["win"] = win;
        }
        if (mac) {
            cmd["bindKey"]["mac"] = mac;
        }
        if (scrollIntoView) {
            if (["animate", "center", "cursor", "selectionPart"].indexOf(scrollIntoView) !== -1) {
                cmd["scrollIntoView"] = scrollIntoView;
            }
        }
        if (multiSelectAction) {
            if (["forEach", "forEachLine", "single"].indexOf(multiSelectAction) !== -1) {
                cmd["multiSelectAction"] = multiSelectAction;
            }
        }
        if (typeof readOnly == "boolean") {
            cmd["readOnly"] = readOnly;
        }
        return cmd;
    }
    function setup_keybinds() {
        function win(key, ctrl, shift, alt) {
            var binds = [];
            if (ctrl) {
                binds.push("ctrl");
            }
            if (shift) {
                binds.push("shift");
            }
            if (alt) {
                binds.push("alt");
            }
            binds.push(key);
            return binds.join("-");
        }
        function mac(key, cmd, shift, option) {
            var binds = [];
            if (cmd) {
                binds.push("cmd");
            }
            if (shift) {
                binds.push("shift");
            }
            if (option) {
                binds.push("option");
            }
            binds.push(key);
            return binds.join("-");
        }
        var cmds = [
            [
                "save",
                "Save File",
                function () {
                    save_file();
                },
                win("s", 1),
                mac("s", 1),
            ],
            [
                "save_as",
                "Save As File",
                function () {
                    save_as_file();
                },
                win("s", 1, 1),
                mac("s", 1, 1),
            ],
            [
                "open",
                "Open File",
                open_file,
                win("o", 1),
                mac("o", 1),
            ],
            [
                "print",
                "Print File",
                print,
                win("p", 1),
                mac("p", 1),
            ],
            [
                "history",
                "File History",
                file_history,
                win("h", 1),
                mac("h", 1),
            ],
            [
                "bookmark",
                "Bookmark",
                bookmark,
                win("b", 1),
                mac("b", 1),
            ],
            [
                "togglebookmark",
                "Toggle Bookmark",
                function () {
                    bm_toggle(window.location.hash.slice(1));
                },
                win("b",0, 0, 1),
                mac("b",0, 0, 1),
            ],
            [
                "opennewtab",
                "Open New Tab",
                function () {
                    window.open("/");
                },
                win("t", 0, 0, 1),
                mac("t", 0, 0, 1),
            ],
            [
                "duplicatetab",
                "Duplicate Tab",
                function () {
                    window.open("/"+window.location.hash);
                },
                win("d", 0, 0, 1),
                mac("d", 0, 0, 1),
            ],
            [
                "replace2",
                "Replace Text",
                function(){
                    editor.execCommand("replace");
                },
                win("r", 1),
                mac("r", 1),
            ],
            [
                "gotoline",
                "Goto Line",
                gotoline,
                win("g", 1),
                mac("g", 1),
                0,
                0,
                true
            ],
            [
                "duplicate",
                "Duplicate Text",
                function(){
                    editor.duplicateSelection();
                },
                win("d", 1),
                mac("d", 1),
                "cursor",
                "forEach",
            ],
            [
                "removeline",
                "Remove Line",
                function(){
                    editor.removeLines();
                },
                win("d", 1, 1),
                mac("d", 1, 1),
                "cursor",
                "forEachLine",
            ],
            [
                "addcursorabove",
                "Add Cursor Above",
                function () {
                    editor.selectMoreLines(-1);
                },
                win("up", 1, 1),
                mac("up", 1, 1),
                0,
                0,
                true
            ],
            [
                "addcursorbelow",
                "Add Cursor Below",
                function () {
                    editor.selectMoreLines(1);
                },
                win("down", 1, 1),
                mac("down", 1, 1),
                0,
                0,
                true
            ],
            [
                "addlineabove",
                "Add Line Above",
                function () {
                    var row = editor.session.selection.lead.row+1;
                    editor.session.insert({
                        "row": row-1,
                        "column": 0
                    }, "\n");
                    editor.gotoLine(row);
                },
                win("return", 0, 1),
                mac("return", 0, 1),
                "cursor",
                "forEachLine",
            ],
            [
                "addlinebelow",
                "Add Line Below",
                function () {
                    var row = editor.session.selection.lead.row+1;
                    editor.session.insert({
                        "row": row-1,
                        "column": editor.session.getLine(row-1).length
                    }, "\n");
                    editor.gotoLine(row+1);
                },
                win("return", 1),
                mac("return", 1),
                "cursor",
                "forEachLine",
            ],

        ];
        var url_blacklist_cmds = [
            "save",
            "save_as",
            "open",
            "history",
            "bookmark",
            "togglebookmark"
        ];
        var safe_keybinds = [
            "ctrl-y","cmd-y",
            "ctrl-z", "cmd-z",
            "ctrl-f", "cmd-f",
            "up","down","left","right",
            "alt-up","alt-down",
            "ctrl-left","ctrl-right","cmd-left","cmd-right",
            "shift-up","shift-down","shift-left","shift-right",
            "ctrl-shift-left","ctrl-shift-right","cmd-shift-left","cmd-shift-right",
            "pageup","pagedown",
            "shift-pageup","shift-pagedown",
            "ctrl-/","cmd-/",
            "home","end",
            "ctrl-home","ctrl-end","cmd-home","cmd-end",
            "shift-home","shift-end",
            "ctrl-shift-home","ctrl-shift-end","cmd-shift-home","cmd-shift-end",
            "tab","shift-tab",
            "ctrl-a","cmd-a",
            "shift-a",
            "backspace",
            "delete",
        ];
        for (var kb in editor.keyBinding.$defaultHandler.commandKeyBinding) {
            if (safe_keybinds.indexOf(kb) === -1) {
                delete editor.keyBinding.$defaultHandler.commandKeyBinding[kb];
            }
        }
        for (var i=0; i<cmds.length; i++) {
            if (window.location.search.split("url=").length === 2) {
                if (url_blacklist_cmds.indexOf(cmds[i][0]) !== -1) {
                    continue;
                }
            }
            editor.commands.addCommand(build_cmds(cmds[i]));
        }
        console.log("Key Binds", editor.keyBinding.$defaultHandler.commandKeyBinding);
    }
    function setup_linesep(linesep) {
        $("div#linesepselect > div").removeClass("highlight");
        $("div#linesepselect > div[data-sep='"+linesep.toLowerCase()+"']").addClass("highlight");
        $("div#statusbar .linesep").html(linesep.padEnd(4, " ").replace(/ /g, "&nbsp;")).off("click").click(function () {
            var linesepselect = $("div#linesepselect");
            if (linesepselect.is(":visible")){
                linesepselect.hide();
            }
            else {
                var offset = $(this).offset();
                linesepselect.show(0, function() {
                    offset.top = "calc(100vh - 4vh - 5px - " + linesepselect.height() + "px)";
                    linesepselect.css(offset);
                });
            }
        });
    }
    function load_file(){
        function guess_mode(f){
            return modelist.getModeForPath(f).mode;
        }
        if (window.location.hash.slice(1)){
            prev_hash = window.location.hash.slice(1);
            var f = decodeURIComponent(window.location.hash.slice(1));
            editor.session.setMode(guess_mode(f));
            backup_post(api_url, {"file": f}, function (response) {
                response = decodeURIComponent(atob(response));
                last_path = f.split("/").slice(0, -1).join("/");
                original_text = response;
                $("div#statusbar .statustext").html("File loading ...");
                editor.session.setUseSoftTabs(true);
                editor.session.setValue(response, -1);
                var sep = response.match(/(\r\n|[\r\n])/g)||["\n"];
                var linesep = "LF";
                if (sep[0] === "\r\n") {
                    linesep = "CRLF";
                }
                else if (sep[0] === "\r") {
                    linesep = "CR";
                }
                setup_linesep(linesep);
                set_status("File loaded.");
                $("title").html("ACE - "+f.split("/").slice(-1)[0]);
            }).fail(function (response) {
                original_text = "";
                editor.session.setValue("", -1);
                set_status("File failed to load. Reason: "+response.responseText);
                $("div#statusbar .linesep").text("LF");
            });
        }
        else {
            setup_linesep("LF");
            original_text = "";
            function callback(v, error){
                editor.session.setValue(v, -1);
                var status = "Editor loaded. Text mode. Temp mode. Open or New file to continue.";
                if (error) {
                    status += error;
                }
                set_status(status);
            }
            var url = window.location.search.split("url=");
            if (url.length === 2) {
                url = url.slice(-1)[0];
                editor.session.setMode(guess_mode(url));
                $.get(url, callback).fail(function(){
                    callback("", " Failed to get file from url.");
                });
            }
            else {
                callback("");
            }
        }
    }
    function setup_events() {
        window.onhashchange = function(){
            if (window.location.hash.slice(1) === prev_hash) {
                return;
            }
            if (editor.session.getValue() !== original_text) {
                if (!confirm(onbeforeunload())) {
                    window.location.hash = "#"+prev_hash;
                    return;
                }
            }
            load_file();
        }
        $("div#dialog div.close").click(function () {
            $("div#dialog > *:not(div.close)").remove();
            $("div#dialog").hide();
        });
        $("div#statusbar .statustext").click(function () {
            alert($(this).text());
        });
        $("div#statusbar .ace_status-indicator").click(gotoline);
        $("div#linesepselect > div").click(function () {
            var linesep = $(this).data("sep");
            if ($("div#statusbar .linesep").text() === "???" && !confirm("Are you sure to replace all CR and LF to "+linesep.toUpperCase()+"?")){
                return;
            }
            setup_linesep(linesep.toUpperCase());
            linesep = linesep.replace("cr", "\r").replace("lf", "\n");
            var content = editor.session.getValue();
            content = content.replace(/\r\n/g, "\n").replace(/\r/g, "\n").split("\n");
            content = content||[];
            content = content.join(linesep);
            editor.session.setValue(content, -1);
            $(this).parent().hide();
        });
    }
    var statusbarto;
    var last_path = "/";
    set_status("Editor loading ...");
    var original_text = "";
    var onbeforeunload = function(){
        return "File is changed.\nAre you sure you want to leave?";
    };
    var modelist = ace.require("ace/ext/modelist");
    var btns = {};
    var wrap_setting = true;
    var editor = ace.edit("editor");
    var prev_hash = window.location.hash.slice(1);
    build_toolbar();
    editor.setFontSize(16);
    editor.setOption("indentedSoftWrap", false);
    editor.setOption("wrap", wrap_setting);
    editor.setTheme("ace/theme/tomorrow_night_bright");
    var StatusBar = ace.require("ace/ext/statusbar").StatusBar;
    var statusbar = new StatusBar(editor, $("div#statusbar").get(0));
    setup_keybinds();
    setup_events();
    load_file();
    setInterval(function () {
        if ($("div#statusbar .statustext").html().indexOf("failed") !== -1) return;
        var v = editor.session.getValue();
        if (!v) return;
        var _ = v!==original_text;
        if (_) {
            var why = ""
            if (editor.session.getUndoManager().isClean()) {
                why = " (Probably due to changed/unified line separators)";
            }
            set_status("File changed."+why+" Size change: "+(v.length-original_text.length));
        }
        else {
            set_status("File not changed.")
        }
        window.onbeforeunload = _?onbeforeunload:null;
    }, 500);
});
