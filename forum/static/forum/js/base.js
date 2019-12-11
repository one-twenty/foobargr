// Dropdown at profile
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, {
        coverTrigger: false,
    });
});

// Dropdown at categories
document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.dropdown-trigger-categories');
    var instances = M.Dropdown.init(elems, {
        hover: true,
        coverTrigger: false,
    });
});

// Sidebar
document.addEventListener("DOMContentLoaded", function() {
    var elems = document.querySelectorAll(".sidenav");
    var instances = M.Sidenav.init(elems);
});
