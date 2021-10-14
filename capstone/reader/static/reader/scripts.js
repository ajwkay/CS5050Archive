document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll(".edit_button").forEach(function(button) {
    button.onclick = function() {
      reviewID = button.dataset.pk;
      storyfolderID = button.dataset.story;
      document.querySelector('#review-rating' + reviewID).innerHTML = "";
      $('#review-rating' + reviewID).attr('class', '');
      document.querySelector('#ebod' + reviewID).innerHTML = "<p style='margin-bottom: 3px;'><label for='new_rating'>Rating:&nbsp;</label><select id='new_rating' name='new_rating'><option value=1>1</option><option value=2>2</option><option value=3>3</option><option value=4>4</option><option value=5>5</option><option value=6>6</option><option value=7>7</option><option value=8>8</option><option value=9>9</option><option value=10>10</option></select>★</p><input hidden type='text' name='reviewID' id='reviewID' value=" + reviewID + "><input hidden type='text' name='storyfolderID' id='storyfolderID' value=" + storyfolderID + "><textarea name='new_body' id='" + reviewID + "' rows='5' cols='90%'></textarea><p><input type='submit' value='Submit'></p>";
      document.querySelector('#ebut' + reviewID).innerHTML = "";
    }
  });
});

document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll(".intro_edit").forEach(function(button) {
    button.onclick = function() {
      profileID = button.dataset.pk;
      $('.profile_intro').html("<input hidden type='text' name='profile_id' id='profile_id' value=" + profileID + "><textarea name='new_intro' id='new_intro' rows='5' cols='90%'></textarea><p><input type='submit' value='Submit'></p>");
      $('.intro_edit').html("");
    }
  });
});

$(document).ready(function() {
  $('.intro_edit_area').submit(function() {
    $.ajax({
      data: $(this).serialize(),
      type: $(this).attr('method'),
      url: $(this).attr('action'),
      success: function(response) {
        $('.intro_edit').html(`<u>[Edit]</u>`);
        if (response.new_intro) {
          $('.profile_intro').css('color', 'black');
          $('.profile_intro').html(response.new_intro);
        } else {
          $('.profile_intro').css('color', 'grey');
          $('.profile_intro').html("(Profile intro goes here.)");
        }
      }
    });
    return false;
  });
});


$(document).ready(function() {
  $('.edit_form').submit(function() {
    $.ajax({
      data: $(this).serialize(),
      type: $(this).attr('method'),
      url: $(this).attr('action'),
      success: function(response) {
        $('#review-rating' + response.reviewID).html(`${response.new_rating}★`);
        $('#ebod' + response.reviewID).html(`<p class="review-body">${response.new_body}</p>`);
        $('#ebut' + response.reviewID).html("[Edit] &nbsp;•&nbsp;");
        $('#' + response.reviewID + ".like_button").html(response.new_button);
        $('#avg_rating').html(`${response.new_avg_rating.toFixed(2)}★`);
        if (response.new_rating == 1 || response.new_rating == 2) {
          $('#review-rating' + response.reviewID).attr('class', 'review-rating-lowest');
        } else if (response.new_rating == 3 || response.new_rating == 4) {
          $('#review-rating' + response.reviewID).attr('class', 'review-rating-low');
        } else if (response.new_rating == 5 || response.new_rating == 6) {
          $('#review-rating' + response.reviewID).attr('class', 'review-rating-mid');
        } else if (response.new_rating == 7 || response.new_rating == 8) {
          $('#review-rating' + response.reviewID).attr('class', 'review-rating-high');
        } else if (response.new_rating == 9 || response.new_rating == 10) {
          $('#review-rating' + response.reviewID).attr('class', 'review-rating-highest');
        };
        if (response.new_avg_rating <= 2.0) {
          $('#avg_rating').attr('class', 'avg-rating-lowest');
        } else if (response.new_avg_rating > 2.0 && response.new_avg_rating <= 4.0) {
          $('#avg_rating').attr('class', 'avg-rating-low');
        } else if (response.new_avg_rating > 4.0 && response.new_avg_rating <= 6.0) {
          $('#avg_rating').attr('class', 'avg-rating-mid');
        } else if (response.new_avg_rating > 6.0 && response.new_avg_rating <= 8.0) {
          $('#avg_rating').attr('class', 'avg-rating-high');
        } else if (response.new_avg_rating >= 8.0) {
          $('#avg_rating').attr('class', 'avg-rating-highest');
        };
      }
    });
    return false;
  });
});

$(document).ready(function() {
    $('.like_form').submit(function() {
        $.ajax({
            data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
                $('#' + response.id + ".like_button").html(response.new_button);
            }
        });
        return false;
    });
});

function gotoCat(obj) {
  genre = obj.className.slice(10).toUpperCase();
  location.href=`/category/genre/${genre}`
}
