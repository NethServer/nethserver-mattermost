$(document).on("nethserver-loaded", function () {
    // define app routing
    var app = $.sammy('#app-views', function () {
        this.use('Template');

        this.get('#/', function (context) {
            context.app.swap('');
            localStorage.setItem("mattermost-path", '');
            context.render('views/dashboard.html', {})
                .appendTo(context.$element());
        });

        this.get('#/configuration', function (context) {
            context.app.swap('');
            localStorage.setItem("mattermost-path", 'configuration');
            context.render('views/configuration.html', {})
                .appendTo(context.$element());
        });

        this.get('#/logs', function (context) {
            context.app.swap('');
            localStorage.setItem("mattermost-path", 'logs');
            context.render('views/logs.html', {})
                .appendTo(context.$element());
        });

        this.get('#/about', function (context) {
            context.app.swap('');
            localStorage.setItem("mattermost-path", 'about');
            context.render('views/about.html', {})
                .appendTo(context.$element());
        });

        this.before('.*', function () {
            var hash = document.location.hash.replace("/", "");
            hash = hash == '#' ? '#dashboard' : hash
            $("nav>ul>li").removeClass("active");
            $("nav>ul>li" + hash + "-item").addClass("active");
        });

    });

    var path = localStorage.getItem("mattermost-path") || '';
    app.run('#/' + path);

    /* i18n */
    $('[i18n]').each(function () {
        $(this).text(_($(this).attr('i18n')))
    });
    /* */
})

function byteFormat(size) {
    var result;

    switch (true) {
        case size === null || size === "" || isNaN(size):
            result = "-";
            break;

        case size >= 0 && size < 1024:
            result = size + " B";
            break;

        case size >= 1024 && size < Math.pow(1024, 2):
            result = Math.round(size / 1024 * 100) / 100 + " K";
            break;

        case size >= Math.pow(1024, 2) && size < Math.pow(1024, 3):
            result = Math.round(size / Math.pow(1024, 2) * 100) / 100 + " M";
            break;

        case size >= Math.pow(1024, 3) && size < Math.pow(1024, 4):
            result = Math.round(size / Math.pow(1024, 3) * 100) / 100 + " G";
            break;

        default:
            result = Math.round(size / Math.pow(1024, 4) * 100) / 100 + " T";
    }

    return result;
}
