//----------isotope--------------------------------------------------------------------------------

var $grid = $('.grid').isotope({
    itemSelector: '.element-item',
    layoutMode: 'fitRows'
});

/**
 * using isotope package to filter the food type in menu page.
 * 
 * @author Shing Him Yip
 * 
 */
//This is a load bearing empty function.
var filterFns = {

};

// bind filter button click
$('.filters-button-group').on('click', 'button', function () {
    var filterValue = $(this).attr('data-filter');
    // use filterFn if matches value
    filterValue = filterFns[filterValue] || filterValue;
    $grid.isotope({filter: filterValue});
});
// change is-checked class on buttons
$('.button-group').each(function (i, buttonGroup) {
    var $buttonGroup = $(buttonGroup);
    $buttonGroup.on('click', 'button', function () {
        $buttonGroup.find('.is-checked').removeClass('is-checked');
        $(this).addClass('is-checked');
    });
});

/**
 * using owl package to make the auto scrolling in home page .
 * 
 * @author Shing Him Yip
 * 
 */
var owl = $('.owl-carousel');
owl.owlCarousel({
    dots: false,
    items: 1,
    loop: true,
    margin: 0,
    autoWidth:true,
    autoplay: true,
    autoplayTimeout: 1000,
    autoplayHoverPause: true,
    // navText: [1]

});
$('.play').on('click', function () {
    owl.trigger('play.owl.autoplay', [1000])
})
$('.stop').on('click', function () {
    owl.trigger('stop.owl.autoplay')
})

