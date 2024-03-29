// Scroll to the top
let mybutton = document.getElementById("btn-back-to-top");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function () {
  scrollFunction();
};

function scrollFunction() {
  if (
    document.body.scrollTop > 20 ||
    document.documentElement.scrollTop > 20
  ) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
// When the user clicks on the button, scroll to the top of the document
mybutton.addEventListener("click", backToTop);

function backToTop() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}

// Academy Modal

$(document).ready(function () {
  $('.iframe-preview').click(function () {

    var attributeDomain = $(this).data('attributedomain');
    console.log(attributeDomain)
    var attributeLink = $(this).data('attributelink');

    $('#sourceName').text(attributeDomain + ' Preview');
    $('#iframeUrl').attr('src', attributeLink);
  });
});
