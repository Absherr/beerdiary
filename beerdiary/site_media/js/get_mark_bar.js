function get_mark_bar(value, id)
{
    cm = parseFloat(value)
    marked_div = "";
    if(cm==0)
        marked_div = "<div class='gray_mark_bar' title='?/5'></div>";
    else
    {
        w = parseInt(cm * 25 - 25);
        marked_div="<div style='width:"+w+"px;' class = 'green_mark_bar' title='"+cm+"/5'></div>"
    }
    return '<div id="mark_'+id+'" class="red_mark_bar" title="'+cm+'/5">'+marked_div+"</div>"
}