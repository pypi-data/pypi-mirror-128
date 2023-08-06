$(document).ready(function () {
    $('.menu > .sidebar-item').each(function (index, elem) {
        console.log($(elem).find('a').attr('href').split('/').reverse()[1]);
        if (window.location.pathname.split('/').reverse()[1] === $(elem).find('a').attr('href').split('/').reverse()[1]){
            $(elem).toggleClass('active');

        }

    });
    $('.menu > .sidebar-item.has-sub').each(function (index, elem) {

        // if (window.location.pathname.split('/')[2] === $(elem).find('a').attr('href').split('/')[2]){
        //     $(elem).toggleClass('active');
        // }
        $(elem).find('.submenu-item').each(function (index, sub_elem) {
            if (window.location.pathname.split('/')[3] === $(sub_elem).find('a').attr('href').split('/')[3]){
                $(elem).find('.submenu').toggleClass('active');
                $(sub_elem).toggleClass('active');
            }
        })

    });
});