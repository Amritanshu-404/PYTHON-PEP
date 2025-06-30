console.log("Hello Me");
window.alert("Hello");

var name = prompt('Enter Your Name : ');
var subject = prompt("What Subject You are Learning : ");

var container = document.getElementById('output');

container.innerHTML += "Hello 😀 " + name + ".<br>";


if (subject == 'Python')
    container.innerHTML += "You are Attending Right Class.<br>";
else
    container.innerHTML += "You are Attending Wrong Class Bro.<br>";


var day = "mon";

switch (day) {
    case "mon":
    case "tue":
    case "wed":
    case "thu":
    case "fri":
        container.innerHTML += "Working Day";
        break;
    case "sat":
    case "sun":
        container.innerHTML += "Holiday";
        break;
    default:
        container.innerHTML += "Invalid day";
}
