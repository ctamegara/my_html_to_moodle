# my_html_to_moodle
some programs to make life easy


To write a section, here is how I do :

<ul>
<li> I write in a customized simple html style in a .html file. See Example.html for an example.</li>

<li> Then I run the function "transform("Example.html")" from the "my_html_to_tek.py" file. </li>

<li> This creates a new html file with the same name prefixed by "tek_", such as 'tek_Example.html".</li>

<li> Then I copy-paste the content of this file in the corresponding section on moodle. (In fact this is automated with selenium, 
but the code is too ugly for the moment, I will share it when it will have been cleaned).</li>

</ul>

It goes faster than writing directly on moodle, and it is very flexible : you can write codes, 
quizes, problems with the solution in a dropdown, in just a few lines. You can customize all the styles.

The code has been written "on the fly", so it's not beautiful, but it works.


