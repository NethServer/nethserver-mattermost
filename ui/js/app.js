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
            result = Math.round(size / 1024 * 100) / 100 + " KB";
            break;

        case size >= Math.pow(1024, 2) && size < Math.pow(1024, 3):
            result = Math.round(size / Math.pow(1024, 2) * 100) / 100 + " MB";
            break;

        case size >= Math.pow(1024, 3) && size < Math.pow(1024, 4):
            result = Math.round(size / Math.pow(1024, 3) * 100) / 100 + " GB";
            break;

        default:
            result = Math.round(size / Math.pow(1024, 4) * 100) / 100 + " TB";
    }

    return result;
}

function humanFormat(number, decimals = false) {
    var result;

    switch (true) {
        case number === null || number === "" || isNaN(number):
            result = "-";
            break;

        case number >= 0 && number < 1000:
            result = number;
            break;

        case number >= 1000 && number < Math.pow(1000, 2):
            if (decimals) {
                result = Math.round(number / 1000 * 10) / 10 + " K";
            } else {
                result = Math.round(number / 1000) + " K";
            }
            break;

        case number >= Math.pow(1000, 2) && number < Math.pow(1000, 3):
            if (decimals) {
                result = Math.round(number / Math.pow(1000, 2) * 10) / 10 + " M";
            } else {
                result = Math.round(number / Math.pow(1000, 2)) + " M";
            }
            break;

        case number >= Math.pow(1000, 3) && number < Math.pow(1000, 4):
            if (decimals) {
                result = Math.round(number / Math.pow(1000, 3) * 10) / 10 + " B";
            } else {
                result = Math.round(number / Math.pow(1000, 3)) + " B";
            }
            break;

        default:
            if (decimals) {
                result = Math.round(number / Math.pow(1000, 4) * 10) / 10 + " T";
            } else {
                result = Math.round(number / Math.pow(1000, 4)) + " T";
            }
    }
    return result;
}
