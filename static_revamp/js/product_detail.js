$(document).ready(function() {
  var largeImage = document.querySelector("#main_product_image #large_img");
  var tinyImages = document.querySelectorAll(".product_image_small img");
  tinyImages[0].classList.add('selected')
  var tinyImagesContainer = document.querySelector(
    "#product_images_small > div"
  );
  var tinyImagesList = [...tinyImages];

  const clearSelectedImage = () => {
    if (
      document.querySelectorAll(".product_image_small img.selected").length > 0
    ) {
      document
        .querySelectorAll(".product_image_small img.selected")[0]
        .classList.remove("selected");
    }
  };

  tinyImages.forEach(tinyImage => {
    tinyImage.addEventListener("click", e => {
      largeImage.src = e.target.src;
      clearSelectedImage();
      e.target.classList.add("selected");
    });
  });

  var largeLeftArrow = document.querySelector(".large-left");
  var largeRightArrow = document.querySelector(".large-right");
  var smallLeftArrow = document.querySelector(".small-left");
  var smallRightArrow = document.querySelector(".small-right");

  largeLeftArrow.addEventListener("click", () => {
    if (tinyImages[0].classList.contains("selected")) {
      return;
    } else {
      var indexOfSelected = tinyImagesList.indexOf(
        document.querySelector(".product_image_small img.selected")
      );
      clearSelectedImage();
      var previousTinyImage = tinyImages[indexOfSelected - 1];
      previousTinyImage.classList.add("selected");
      largeImage.src = previousTinyImage.src;
    }
  });
  largeRightArrow.addEventListener("click", () => {
    if (tinyImages[tinyImages.length - 1].classList.contains("selected")) {
      return;
    } else {
      var indexOfSelected = tinyImagesList.indexOf(
        document.querySelector(".product_image_small img.selected")
      );
      clearSelectedImage();
      var previousTinyImage = tinyImages[indexOfSelected + 1];
      previousTinyImage.classList.add("selected");
      largeImage.src = previousTinyImage.src;
    }
  });

  smallLeftArrow.addEventListener("click", () => {
    tinyImagesContainer.scrollLeft -= 50;
  });

  smallRightArrow.addEventListener("click", () => {
    tinyImagesContainer.scrollLeft += 50;
  });

  // yay..jquery
  $(".show_features").click(function() {
    $(".ads_backdrop").show();
  });
  $(".ads_backdrop").click(function() {
    $(this).hide();
  });
});
