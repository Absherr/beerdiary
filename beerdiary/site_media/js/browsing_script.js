function add_to_view(first_letter, should_be_with_marks)
{
    if ($("#first_letters").has('#link'+first_letter).length)
    {}
    else
    {
        $('#first_letters').append('<a id="link'+first_letter+'" href="#letter'+first_letter+'">' +
            ''+first_letter+' </a>');
    }
    if ($("#list").has('#letter'+first_letter).length)
    {}
    else
    {
        to_append = '<h2 class="capitalLetter">' + first_letter + '</h2>' +
            '<div id="letter' + first_letter + '" name = "letter' + first_letter + '">' +
            '<div id="list' + first_letter + '" style="width: 40%; float: left;"></div>';
        if(should_be_with_marks==true)
            to_append += '<div id="marks' + first_letter + '" style="width: 60%; float: right;"></div>';
        to_append += '</div>';
        $('#list').append(to_append);
    }
}
