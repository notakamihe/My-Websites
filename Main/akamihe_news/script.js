holidays = {
    "November 26": "Happy Thanksgiving",
    "December 25": "Merry Christmas",
    "January 1": "Happy New Year",
    "January 18": "Martin Luther King Day",
    "February 1": "Day 1 of Black History Month",
    "February 2": "Groundhog Day",
    "February 14": "Valentine's Day",
    "February 15": "President's Day",
    "March 17": "St. Patrick's Day",
    "April 1": "April Fool's Day",
    "April 4": "Easter",
    "May 5": "Cinco De Mayo",
    "May 10": "Mother's Day",
    "May 31": "Memorial Day",
    "June 20": "Summer & Father's Day",
    "July 4": "Independence Day",
    "September 6": "Labor Day",
    "September 12": "Grandparent's Day",
    "October 10": "Indigenous People's Day",
    "October 31": "Happy Halloween"
};

let monthName;
let monthDate;
let dayOfTheWeek;
let currentTime;

updateTime();

if (monthDate in holidays) {
    let holidayText = document.createElement("p");
    holidayText.innerHTML = holidays[monthDate];
    document.querySelector(".header-auxiliary-content").appendChild(holidayText);
}

setInterval(updateTime, 1000);

function updateTime ()
{
    monthName = getMonthName(new Date().getMonth());
    monthDate = `${monthName} ${new Date().getDate()}`;
    dayOfTheWeek = getDayName(new Date().getDay());
    currentTime = new Date().toLocaleTimeString();

    Array.from(document.querySelectorAll(".date")).forEach(item => {
        item.innerHTML = `${dayOfTheWeek} ${new Date().getDate()} ${monthName} ${new Date().getFullYear()} 
        ${currentTime}`;
    });

    
}

function getMonthName (monthNum) {
    monthNames = [
        "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ];

    monthInteger = parseInt(monthNum);

    if (monthInteger < 0 || monthInteger > 11) {
        console.log("Month number invalid.");
        return null;
    }

    return monthNames[monthInteger];
}

function getDayName (dayNum) {
    daysOfTheWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    if (dayNum < 0 || dayNum > 6) {
        console.log("Week number invalid.");
        return;
    }

    return daysOfTheWeek[dayNum];
}