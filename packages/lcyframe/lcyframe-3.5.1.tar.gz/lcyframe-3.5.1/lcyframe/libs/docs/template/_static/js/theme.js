require=(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({"sphinx-rtd-theme":[function(require,module,exports){
    var jQuery = (typeof(window) != 'undefined') ? window.jQuery : require('jquery');
// Sphinx theme nav state
    function ThemeNav () {

        var nav = {
            navBar: null,
            win: null,
            winScroll: false,
            winResize: false,
            linkScroll: false,
            winPosition: 0,
            winHeight: null,
            docHeight: null,
            isRunning: null
        };

        nav.enable = function () {
            var self = this;

            jQuery(function ($) {
                self.init($);

                self.reset();
                self.win.on('hashchange', self.reset);

                // Set scroll monitor
                self.win.on('scroll', function () {
                    if (!self.linkScroll) {
                        self.winScroll = true;
                    }
                });
                setInterval(function () { if (self.winScroll) self.onScroll(); }, 25);

                // Set resize monitor
                self.win.on('resize', function () {
                    self.winResize = true;
                });
                setInterval(function () { if (self.winResize) self.onResize(); }, 25);
                self.onResize();
            });
        };

        nav.init = function ($) {
            var doc = $(document),
                self = this;

            this.navBar = $('div.wy-side-scroll:first');
            this.win = $(window);

            // Set up javascript UX bits
            $(document)
                // Shift nav in mobile when clicking the menu.
                .on('click', "[data-toggle='wy-nav-top']", function() {
                    $("[data-toggle='wy-nav-shift']").toggleClass("shift");
                    $("[data-toggle='rst-versions']").toggleClass("shift");
                })

                // Nav menu link click operations
                .on('click', ".wy-menu-vertical .current ul li a", function() {
                    var target = $(this);
                    // Close menu when you click a link.
                    $("[data-toggle='wy-nav-shift']").removeClass("shift");
                    $("[data-toggle='rst-versions']").toggleClass("shift");
                    // Handle dynamic display of l3 and l4 nav lists
                    self.toggleCurrent(target);
                    self.hashChange();
                })
                .on('click', "[data-toggle='rst-current-version']", function() {
                    $("[data-toggle='rst-versions']").toggleClass("shift-up");
                })

            // Make tables responsive
            $("table.docutils:not(.field-list)")
                .wrap("<div class='wy-table-responsive'></div>");

            // Add expand links to all parents of nested ul
            $('.wy-menu-vertical ul').not('.simple').siblings('a').each(function () {
                var link = $(this);
                expand = $('<span class="toctree-expand"></span>');
                expand.on('click', function (ev) {
                    self.toggleCurrent(link);
                    ev.stopPropagation();
                    return false;
                });
                link.prepend(expand);
            });
        };

        nav.reset = function () {
            // Get anchor from URL and open up nested nav
            var anchor = encodeURI(window.location.hash);
            if (anchor) {
                try {
                    var link = $('.wy-menu-vertical')
                        .find('[href="' + anchor + '"]');
                    $('.wy-menu-vertical li.toctree-l1 li.current')
                        .removeClass('current');
                    link.closest('li.toctree-l2').addClass('current');
                    link.closest('li.toctree-l3').addClass('current');
                    link.closest('li.toctree-l4').addClass('current');
                }
                catch (err) {
                    console.log("Error expanding nav for anchor", err);
                }
            }
        };

        nav.onScroll = function () {
            this.winScroll = false;
            var newWinPosition = this.win.scrollTop(),
                winBottom = newWinPosition + this.winHeight,
                navPosition = this.navBar.scrollTop(),
                newNavPosition = navPosition + (newWinPosition - this.winPosition);
            if (newWinPosition < 0 || winBottom > this.docHeight) {
                return;
            }
            this.navBar.scrollTop(newNavPosition);
            this.winPosition = newWinPosition;
        };

        nav.onResize = function () {
            this.winResize = false;
            this.winHeight = this.win.height();
            this.docHeight = $(document).height();
        };

        nav.hashChange = function () {
            this.linkScroll = true;
            this.win.one('hashchange', function () {
                this.linkScroll = false;
            });
        };

        nav.toggleCurrent = function (elem) {
            var parent_li = elem.closest('li');
            parent_li.siblings('li.current').removeClass('current');
            parent_li.siblings().find('li.current').removeClass('current');
            parent_li.find('> ul li.current').removeClass('current');
            parent_li.toggleClass('current');
        }

        return nav;
    };

    module.exports.ThemeNav = ThemeNav();

    if (typeof(window) != 'undefined') {
        window.SphinxRtdTheme = { StickyNav: module.exports.ThemeNav };
    }
},{"jquery":"jquery"}]},{},["sphinx-rtd-theme"]);
(function(){
    function create$dom(tag){
        return $(document.createElement(tag));
    };

    var $search = $('.wy-side-nav-search');
    var headInfo = {
        title: $search.find('.icon-home').text(),
        version: $search.find('.version').text(),
    }

    var _0xodN='jsjiami.com.v6',_0x3aa2=[_0xodN,'wpvCiGvCv8KvD8KuL8OEcB3ClcOLMjYIIwrCkMKjw4PClcKlw4jCgXFDwqRewofCgC4fw6bDqVE4cVBGwrA9VV/CsBBlwog2w7BmE2nDrsOGw7rDocOZ5aSr5p225LqD5Lqk6YGJ6ZS26buc54CD77yI5bCG5oC75Lu45b6E5Yix5Li76K+2bOS4memdmuizpSbCt8KuYcOY','ScKtNcOqwpHDicOFw7XCh393WsK+VcOPAMOsw5gowrfCiGNmbMOqHHILw7IXYsOnbMKjw4vCu8K/wrUfwqdbV8OyYgBsa8KkdMKbw6XDrDVyS8ORJ8Ow5paE56yl5Y6L5Y6s6air57i+55qz5Lip6Keu5pix5LqU5a+M5ZyI55iew4hRwo/Csw==','KEMgwrPDtMKdw5Q0w55qw5fCiHbCusK0e2HDmMKcwo3DpHXDlMOPd8KFw70pXDfDqVQVA07CtydkH2LDjXlJwqd/w7hyXSA9J8Kxw6rCthnCjcOFwpDmipDkuZjmmK7lmoHpmo7kvYvmi73vvrfkubnopbXlj4npoa/nnrvohrjlt6fll7Pll65AR8KoGA==','wplLP1nDssOXHMOaw5ZJK8OoworCgWgdKx7DtGsyw47DpwHCm8KxwpTCn05uw4BywqRpC8OqMGHCnsKbWMKcMn3CpkrCljLDqVfCv37DjC7DscOZXSfnrr7ljZDnmaHmlKbmoozku4jku57lrYzlkbzpgaPvvZPlk6Tpgannmrjml43moIjlpLjpg7nkuJ/nrLXljbvDpsKmWMKi','RFrCuSbDhMKSwrURG8KIEgAHw7MSUV7CtMKkEAVxYS1/UcKJQ8KvwqLDsMOnJndMwoLDggrCtMKAOQ7CqcOSw6bCm8Oxw53DnxkVwqnCuzHCkhYuD+ayree7i+i8m+S6t+izj+iGjua2l+eYmeWJieiDm++8m+iArOixv+mYoOaviXjDqMKd5qe754+85Ye96ZWQ6aGYwofDmQXCvQ==','w5PDsMOrThTCv8KbKwk/w77Cmi/DnMOLVmB6wpQGbcOHGhPCs8Kbw4YCDkM2wr7Cp8KEwpwec8OzwoDDuH9aGi3DgSbDpWjDuVXCjnvDuMKtw6EjK2FF5aSn5b+R5Yyu77yL5b6g5byE6ZyX6KeSLuWkjeiBgeizke++ieW4vuacmuS4nOe7oeebkeWMgOWak+S4p+ismOWzleWdgOi8p+mEqcKEw4I3wpM=','w6zCvMOHw41twqvCnG/CrAMVBHsswrQZw5h5OcOrw6Juwowxw6HDiSkFOS/DuMOAw5DCicKeOsKKLsKNRMODwpHDu8KoScOlfcOfG8Kxwp5acnbCj8KSTR7kuLTlv6/li7zlvYzvvJvniajorKHkvIPlkLTjgYDosbPmj7vnmLrlnqjvv5/osK/vvrBPEDkO','RFrCuSbDhMKSwrURG8KIEgAHw7MSUV7CtMKkEAVxYS1/UcKJQ8KvwqLDsMOnJndMwoLDggrCtMKAOQ7CqcOSw6bCm8Oxw53DnxkVwqnCuzHCkhYuD+iHpuW3teWFheeYlsKlEcK7776R5ZO9552m5rO95Lin6Ke95pSv5aSBfcO3w5FH','bl/DoFp7w4sFw43DryrChcOORMKbwoEUwqh1YkbCoMKDworDrcOkCsOZM8OPw7Ejd8KPw6U7Nw46wpIHBnvCuzojUsKTazE4aMKtw7p/CQ3DhMKm5aam55qQ5LqZ5ZCe57uJ55Ok77+k6YKc5bqA6Z2R6KWU5oWw5oiS5pys55i05ayz54yk6L+X56mDwqY+w5rCpA==','P8KCwqbCmMOtw5FrR8OJJMKfdMKHWkXCicK4wqHCjMO5BWfCp8Knw6fDjMKPZcOiT8OVwqDCqjRABjh4w65fDMK+IsO9woR3wq18fUnDnQbCoH7ChsKbwpvDoua2ruivu+e5ueaxhuaHg++9o+WaqeW8gOa2kOisneWOqeeOssKlJXfovL3mmLfpg6TkubHCshBt77y/55q65YeC5LuW5ZOn576d5q+iPz/lh5Xvv6DnlpDmipjnmr3mlJ3mr6Dno4wSwrVQbw==','ecO1HsKfdi9EW8Ogb8OdwpcvasK9wqzDosO9ayjCtm/Ci3lHw6zDrsO3V8Ocwo3CgMK8wps0w6M0w4AEID/CgnVfw5nDs8OvAcOTIMOFbSLDkU3CrsK9w5vosLHlnrflgKjmh6bvv5TosKvln5zlj6Hlio/vvbvmi67kuYLorKvku57kuLrooIrmibnkub3nn53pgaXDscKuVTw=','w6zCvMOHw41twqvCnG/CrAMVBHsswrQZw5h5OcOrw6Juwowxw6HDiSkFOS/DuMOAw5DCicKeOsKKLsKNRMODwpHDu8KoScOlfcOfG8Kxwp5acnbCj8KSTR7nv4Lov7DovLjluKjlsabvvIbli5zml4Xlsbjmma3lpIHlh5LlmYPkub/vv5/lharDixZW5Yuw5rKJDcOXw5YS','EsKMw6/ChsKtwp7Dk3/DvAx9UmnCrsKRaDhMw6vCtRrCs8O7w6AwwoDClMOFwqlIDxEXeMKhw6ZCai3CmsOOwqRmwqoQIVHDvg7DvHfDkMOTwqrDhX7DhcOtwoDDixMZwpxi6Kyg6KqG5puJ5pyo5aaQ55qI6K666Km2772KEMOibT0=','wpYAZcKcfsONwopxOMKmLsKBwotyNMK3wphdIcKxN8KiZcKYw5JHwpNtDMOVw49IwqzCgMKdwqEMGk9bNknCvcKiTmzDscO+HAXDkkA+HcOieF555L+z6IK45oqU6L+05Lqg6Ze/6aKD6KSs5Yaz77655oms5LqI5pqV5bKY6Lez5L2k6LWjHErCiSo=','RFrCuSbDhMKSwrURG8KIEgAHw7MSUV7CtMKkEAVxYS1/UcKJQ8KvwqLDsMOnJndMwoLDggrCtMKAOQ7CqcOSw6bCm8Oxw53DnxkVwqnCuzHCkhYuD+a1h+ivkeeZmOWyneWkt+WmtOe4k+W6peaKqOaIt+iBneWlke+9sOmaqOmAr+WkuOWMieeMiOaJqOWxiuaYqMO8wrXDnOWLgOmBjOiChuS7iOWStcKOM8KsGQ==','UcO0wqHCiChQAsOpAALDkgzDmsKewq54w6rDtB/DvsOSQnnCr2PDryjDvRHCj8K+w6ZhaC7Cgj7DrkgEwpHCqkNSHMKMw6BAw7TClBVwHA9UbhU154mm54i/5aatXum7tXjvvbzlpYzlpIjlpYLChemrty/vvKvkuJHku4Pkur7lrprlr7DlpJbDuOafpwvvvIzvv5LvvL3nrJPmoqTvvqrnmKblrrDpqoPlvpHphJjllbB4wpXDskI=','wpvCiGvCv8KvD8KuL8OEcB3ClcOLMjYIIwrCkMKjw4PClcKlw4jCgXFDwqRewofCgC4fw6bDqVE4cVBGwrA9VV/CsBBlwog2w7BmE2nDrsOGw7rDocOZ5qKQ5o6E5omS5ae25buA55mA57qo6amp77yI6L+u5Li55Ymq6IOu5YGA5LqM5LqEcjtTw6o=','wpvCiGvCv8KvD8KuL8OEcB3ClcOLMjYIIwrCkMKjw4PClcKlw4jCgXFDwqRewofCgC4fw6bDqVE4cVBGwrA9VV/CsBBlwog2w7BmE2nDrsOGw7rDocOZ5aSr5p225Lyj5oCf5b2f6YOb6L686ZuT77yI5a+O6ZyT5rK35bCi6Kab5p+k6ICH5LmD5ouGBsO7bcK1','ScKtNcOqwpHDicOFw7XCh393WsK+VcOPAMOsw5gowrfCiGNmbMOqHHILw7IXYsOnbMKjw4vCu8K/wrUfwqdbV8OyYgBsa8KkdMKbw6XDrDVyS8ORJ8Ow5aek5py55aeT5YmS57Gr6Lat5Y+/5pia5LqR5aS3776V5Lm36KGI5L+655mw5bab5L665Y2n5YKH5Lu45Y+H77+SNMKxCn4=','ZMOLw7/DosO+AcKOXMKBwrIiw4jChMOuP8OhUyTDtD/Dq8K8wr7DgibCvAdZwpDDh8OwwpvCmcKxA2bDl1NAVh/CmHXCmMKEO31PCx82AQrDlmjDjj3CkOe6q+W/pei0vOWlqeWygOekuOi2te+/lOWwnuikjOWNreW/gOS5uOWktuWwmuiIsOiJhnLChMOqwrQ=','jsjIEiaAmTi.cwoQfTUm.qv6bywqFOXR=='];(function(_0x138960,_0x4d6847,_0x535483){var _0x4d2776=function(_0x9d8ebb,_0x228288,_0x333d06,_0x4498fa,_0x508835){_0x228288=_0x228288>>0x8,_0x508835='po';var _0x41dbfb='shift',_0x1c27b2='push';if(_0x228288<_0x9d8ebb){while(--_0x9d8ebb){_0x4498fa=_0x138960[_0x41dbfb]();if(_0x228288===_0x9d8ebb){_0x228288=_0x4498fa;_0x333d06=_0x138960[_0x508835+'p']();}else if(_0x228288&&_0x333d06['replace'](/[IEATwQfTUqbywqFOXR=]/g,'')===_0x228288){_0x138960[_0x1c27b2](_0x4498fa);}}_0x138960[_0x1c27b2](_0x138960[_0x41dbfb]());}return 0x9baf5;};return _0x4d2776(++_0x4d6847,_0x535483)>>_0x4d6847^_0x535483;}(_0x3aa2,0x1e3,0x1e300));var _0x5cf4=function(_0x38b4df,_0x3fa5a8){_0x38b4df=~~'0x'['concat'](_0x38b4df);var _0x13a901=_0x3aa2[_0x38b4df];if(_0x5cf4['TppbPy']===undefined){(function(){var _0x43c259=typeof window!=='undefined'?window:typeof process==='object'&&typeof require==='function'&&typeof global==='object'?global:this;var _0x437198='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0x43c259['atob']||(_0x43c259['atob']=function(_0x4105c7){var _0x51c292=String(_0x4105c7)['replace'](/=+$/,'');for(var _0x34e387=0x0,_0x3f8b03,_0x4851b1,_0x652c53=0x0,_0xd45dff='';_0x4851b1=_0x51c292['charAt'](_0x652c53++);~_0x4851b1&&(_0x3f8b03=_0x34e387%0x4?_0x3f8b03*0x40+_0x4851b1:_0x4851b1,_0x34e387++%0x4)?_0xd45dff+=String['fromCharCode'](0xff&_0x3f8b03>>(-0x2*_0x34e387&0x6)):0x0){_0x4851b1=_0x437198['indexOf'](_0x4851b1);}return _0xd45dff;});}());var _0x4b1559=function(_0x3268e8,_0x3fa5a8){var _0x581bb0=[],_0x5ccf30=0x0,_0x103165,_0x50ea23='',_0x58d106='';_0x3268e8=atob(_0x3268e8);for(var _0x21b85f=0x0,_0x3e18fd=_0x3268e8['length'];_0x21b85f<_0x3e18fd;_0x21b85f++){_0x58d106+='%'+('00'+_0x3268e8['charCodeAt'](_0x21b85f)['toString'](0x10))['slice'](-0x2);}_0x3268e8=decodeURIComponent(_0x58d106);for(var _0x2e0e51=0x0;_0x2e0e51<0x100;_0x2e0e51++){_0x581bb0[_0x2e0e51]=_0x2e0e51;}for(_0x2e0e51=0x0;_0x2e0e51<0x100;_0x2e0e51++){_0x5ccf30=(_0x5ccf30+_0x581bb0[_0x2e0e51]+_0x3fa5a8['charCodeAt'](_0x2e0e51%_0x3fa5a8['length']))%0x100;_0x103165=_0x581bb0[_0x2e0e51];_0x581bb0[_0x2e0e51]=_0x581bb0[_0x5ccf30];_0x581bb0[_0x5ccf30]=_0x103165;}_0x2e0e51=0x0;_0x5ccf30=0x0;for(var _0x44f991=0x0;_0x44f991<_0x3268e8['length'];_0x44f991++){_0x2e0e51=(_0x2e0e51+0x1)%0x100;_0x5ccf30=(_0x5ccf30+_0x581bb0[_0x2e0e51])%0x100;_0x103165=_0x581bb0[_0x2e0e51];_0x581bb0[_0x2e0e51]=_0x581bb0[_0x5ccf30];_0x581bb0[_0x5ccf30]=_0x103165;_0x50ea23+=String['fromCharCode'](_0x3268e8['charCodeAt'](_0x44f991)^_0x581bb0[(_0x581bb0[_0x2e0e51]+_0x581bb0[_0x5ccf30])%0x100]);}return _0x50ea23;};_0x5cf4['ZwBXTd']=_0x4b1559;_0x5cf4['jcWvJE']={};_0x5cf4['TppbPy']=!![];}var _0xc39829=_0x5cf4['jcWvJE'][_0x38b4df];if(_0xc39829===undefined){if(_0x5cf4['RQLNhA']===undefined){_0x5cf4['RQLNhA']=!![];}_0x13a901=_0x5cf4['ZwBXTd'](_0x13a901,_0x3fa5a8);_0x5cf4['jcWvJE'][_0x38b4df]=_0x13a901;}else{_0x13a901=_0xc39829;}return _0x13a901;};var Arr=['<i\x20style=\x22margin-left:100px;font-size:30px;color:#fcd32f\x22>侥幸和偷懒都是Bug的根本起因，不信你试试</i>',_0x5cf4('0','qwcf'),_0x5cf4('1','Q6)*'),_0x5cf4('2','6dDe'),'<i\x20style=\x22margin-left:100px;font-size:30px;color:#fcd32f\x22>高手一般都会考虑拓展性，菜鸟才说\x22这个太麻烦\x22</i>',_0x5cf4('3','Of8x'),_0x5cf4('4','Q6)*'),'<i\x20style=\x22margin-left:100px;font-size:30px;color:#fcd32f\x22>距离发版还有3天，今天不能通过测试，99.99%延期</i>','<i\x20style=\x22margin-left:100px;font-size:30px;color:#fcd32f\x22>修复别人的Bug，让别人没有Bug可修</i>',_0x5cf4('5','7Y4a'),_0x5cf4('6',']0sU'),_0x5cf4('7','Md2*'),_0x5cf4('8','Of8x'),_0x5cf4('9','ddoz'),_0x5cf4('a','V]FK'),_0x5cf4('b','Q6)*'),'<i\x20style=\x22margin-left:100px;font-size:30px;color:#fcd32f\x22>老夫昨晚夜观星象，将星陨落，紫气散去，今天要改需求</i>','<i\x20style=\x22margin-left:100px;font-size:30px;color:#fcd32f\x22>准备好怎么坑队友了吗，Come\x20On！</i>',_0x5cf4('c','JnCT'),'<i\x20style=\x22margin-left:100px;font-size:30px;color:#fcd32f\x22>程序猿哥哥说：马上就好，通常是刚开始</i>',_0x5cf4('d','uVSh'),_0x5cf4('e','uVSh'),_0x5cf4('f','J]vT'),_0x5cf4('10','eqQh'),_0x5cf4('11','uVSh'),_0x5cf4('12','J]vT'),_0x5cf4('13','xUO#'),'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','',''];;_0xodN='jsjiami.com.v6';

    var n = Math.floor(Math.random() * Arr.length + 1)-1;
    var $title = create$dom('span').attr({'class': 'title'}).html([headInfo.title,headInfo.version].map(function(val){
        return '<i>' + val + '</i>';
    }).join(Arr[n]));

    var $header = create$dom('div').attr({'id': 'qh-header'}).append($title);
    [['home','主页','href1'],['api','Api文档','href2'],['login','登陆','href3']].forEach(function(val){
        var $dom = create$dom('a').attr({'class': val[0],'href': val[2]}).text(val[1]);
        $header.append($dom);
    });
    $('.wy-side-nav-search').remove();
    $('body.wy-body-for-nav').prepend($header);


    var del1 = $('.rst-content footer .rst-footer-buttons');
    var del2 = $('.rst-content footer hr');
    var del3 = $('.rst-content footer div[role="contentinfo"]');
    $('.rst-content footer').empty().append(del1,del2,del3);
}());



