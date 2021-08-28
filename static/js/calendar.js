window.onload=display_calendar();
function display_calendar()
{
    //日期
    let date_pointer= new Date();
    let now_year=date_pointer.getFullYear();
    let now_month=date_pointer.getMonth();
    let now_date=date_pointer.getDate()//當前日期;
    //天數
    let daysInMonth_leap=[31,29,31,30,31,30,31,31,30,31,30,31];//閏年每月的天數
    let daysInMonth=[31,28,31,30,31,30,31,31,30,31,30,31];//平年每月的天數
    let month_cn=["一月","二月","三月","四月","五月","六月","七月","八月","九月","十月","十一月","十二月"];//平年每月的天數

    let ulOfDays=document.getElementById('calendar-days');
    let calendar_label=document.getElementById('calendar-label');
    let day_list="";

    calendar_label.innerHTML=now_year+"    "+month_cn[now_month];
    //獲取天數  平年：閏年
    const total_days = (now_year%4) ? daysInMonth[now_month] : daysInMonth_leap[now_month];

    //移動到月首
    date_pointer.setDate(1);
    let begin_day=date_pointer.getDay();
    generate_days(begin_day);
    //產生日期
    generate_days(total_days,"normal_day");
    //移動到最後一天
    date_pointer.setDate(total_days);
    let end_day=date_pointer.getDay();
    generate_days(6-end_day);

    function generate_days(times,mode="blank")
    {
        let content=" ";
        let day=new Date();
        for (let i=0;i<times;i++){
            let css_class="list-inline-item calendar-cell border me-1 mt-1";
            day.setDate(i+1);
            if(mode!=="blank")
            {
                content=i+1;
                if((content)===now_date) css_class+=' active';//標示日期
            }
            day_list+="<li class=\'"+css_class+"\' style='white-space:pre;'>"+content+"</li>";
            if (day.getDay()%7==6)
            {
                day_list+="</br>"
            }
        }
    }
    ulOfDays.innerHTML=day_list;
}
