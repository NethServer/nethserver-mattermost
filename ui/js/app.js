$(document).on("nethserver-loaded", function () {
    // define app routing
    var app = $.sammy('#app-views', function () {
        this.use('Template');

        this.get('#/', function (context) {
            context.app.swap('');
            context.render('views/dashboard.html', {})
                .appendTo(context.$element());
        });

        this.get('#/configuration', function (context) {
            context.app.swap('');
            context.render('views/configuration.html', {})
                .appendTo(context.$element());
        });

        this.get('#/logs', function (context) {
            context.app.swap('');
            context.render('views/logs.html', {})
                .appendTo(context.$element());
        });

        this.get('#/about', function (context) {
            context.app.swap('');
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

    app.run('#/');

    /* i18n */
    $('[i18n]').each(function () {
        $(this).text(_($(this).attr('i18n')))
    });
    /* */
})