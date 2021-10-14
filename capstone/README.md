# Interactive Fiction Reader

## **Introduction**

This project, simply named Interactive Fiction (I.F.) Reader, is designed to be a platform for users to submit their I.F. works, as well as browse and read works submitted by other users. While it features many functionalities similar to a social network system, the core focuses of the project are on the **compatibility to host I.F.** works written using different I.F. editors, as well as the **accurate depiction of said works** as part of the web app.

### **Interactive Fiction (I.F.) Works & Editors**

Much like the "choose your own adventure" books of days old, I.F. works can be seen as a halfway mark between video games and books; Stories are told predominantly through text, but readers are allowed the agency to interact with and change the story at set points of the experience. These works usually come in the form of .html files/folder subsystems, and are written using an I.F. editor which takes care of the code for the most part, allowing authors to focus more on the writing. Popular I.F. editors include [Twine](https://twinery.org/), [Squiffy](http://textadventures.co.uk/squiffy), [TADS3](https://www.tads.org/index.htm) and [Quest](http://textadventures.co.uk/quest); each editor produces I.F. files in varyingly different formats from the others. A huge part of this project was thus ensuring works made from different editors could be properly processed and ran despite their format differences.

## Project Files & Instructions

Everything is encompassed in a singular Django app called "reader"; included are the usual essential template, url and views files. User submitted files are stored in the "static" folder, along with the project's .js and .css files. On a side note, a dummy folder is usually created in the base directory when a used submits a file to temporarily store the unzipped contents before moving them to their respective destination folders. A few sample I.F. zip files have been included in the base directory as well for you to try out the process of submitting an I.F. work.

### Using the Application

The project file will already come with a few sample I.F. files (sourced from the internet) already uploaded to it, along with a few registered user accounts to demonstrate the functionalities of the app.

The **index page** acts as a home page, showing all I.F. entries submitted to the site. There will be a few options to **sort** the I.F. entries by different important categories like title, average rating, number of reviews and date submitted. If the user is not **registered** or **logged in**, they can do so via the navigation buttons up top; once logged in all functionalities of the site will be unlocked.

From the home page, users can browse for an I.F. that piques their interest and click on the title to access its **story page**. Once there, the user can click on the **play** button to run and play the I.F. entry. From there, the browser **back button** will bring them back to the story page. Users can also **leave a review** for the I.F. work, rating it from a scale of 1 to 10. Each user may only leave one review on a given I.F. work, but they can **edit** their submitted review later on. They can also **like** reviews submitted by other users to denote the usefulness of the reviews.

Clicking on a user's name (or clicking on profile in the navigation bar) in either of the previously mentioned pages will lead to that user's **profile page**, where one may view their statistics like number of I.F. works submitted, and their top 3 works. Logged in users may choose to **follow** other users here. In the header of the user's top works, one may also click on "**view all**" to see all the works the user has submitted. Users may also leave **comments** on other users' profile pages.

In any place that displays an I.F. work's details, one may see colourful tags denoting the work's main **genre**. Clicking on these tags leads to a page to view I.F. works by whichever genre was clicked.

To **submit** and I.F. work, users can click on "upload" in the navigation bar. The submission will require a title, genre, an abstract, a cover picture, the editor used, as well as the I.F. file itself. The I.F. file has to be encompassed in a zipped folder in either of the mentioned formats on the page. As aforementioned, a few sample I.F. works have been included in the base directory for you to try this out; just ensure that the "editor used" field matches that which is mentioned in each I.F. work's file name.

## Distinctiveness & Complexity

As mentioned before, while this project borrows from a lot of the functionalities from a social network, the main focus is on the submission and hosting of user submitted I.F. files. Much time was spent on analysing and trying to replicate the code format of I.F. files created by different editors to ensure compatibility.

On a technical level, the project does meet the necessary requirements: User profiles, reviews and I.F. entries are all run by Django models in the backend, JavaScript is used for a lot of the user interactions in the front end, and most of the CSS elements are scalable to size to ensure mobile-responsiveness.

Furthermore, because this project implements functionalities not covered in the previous projects, we can consider it to be more complex. Said functionalities include a file upload system which systematically deals with and stores contents of zipped folders, real-time aggregation of average scores, as well as the hosting of external user-customised pages (of course, still limited to certain pre-determined formats).