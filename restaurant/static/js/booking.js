let date = document.getElementById("booking_date").value;

submitButton = document.getElementById("button");
document.getElementById("booking_date").addEventListener("change", function () {
  getBookings();
});

function formatTime(time) {
  const ampm = time < 12 ? "AM" : "PM";
  const t = time < 12 ? time : time > 12 ? time - 12 : time;
  const label = `${t} ${ampm}`;
  return label;
}

function formatDate(date) {
  const d = new Date(date);
  const day = d.getDate() + 1;
  const month = d.getMonth() + 1;
  const year = d.getFullYear();
  return `${day}-${month}-${year}`;
}

function getBookings() {
  let reserved_slots = [];
  date = document.getElementById("booking_date").value;
  document.getElementById("today").innerHTML = " for " + formatDate(date);

  fetch("/api/booking/" + date)
    .then((response) => response.json())
    .then((data) => {
      reserved_slots = [];
      bookings = "";
      for (item of data) {
        console.log(item.fields);
        reserved_slots.push(item.fields.booking_slot);
        bookings += `<p>${item.fields.booking_name} - ${formatTime(
          item.fields.booking_slot
        )}</p>`;
      }

      slot_options = '<option value="0" disabled>Select time</option>';
      for (i = 10; i <= 20; i++) {
        const label = formatTime(i);
        if (reserved_slots.includes(i)) {
          slot_options += `<option value=${i} disabled>${label}</option>`;
        } else {
          slot_options += `<option value=${i}>${label}</option>`;
        }
      }

      document.getElementById("booking_slot").innerHTML = slot_options;
      if (bookings == "") {
        bookings = "No bookings";
      }
      document.getElementById("bookings").innerHTML = bookings;
    });
}

function submitForm() {
  const formdata = {
    user: document.getElementById("username").value,
    date: document.getElementById("booking_date").value,
    time: document.getElementById("booking_time").value,
    guests: document.getElementById("booking_guests").value,
    occasion: document.getElementById("booking_occasion").value,
  };

  fetch("{% url 'bookings' %}", {
    method: "post",
    body: JSON.stringify(formdata),
  })
    .then((r) => r.text())
    .then((data) => {
      getBookings();
    });
}

submitButton.addEventListener("click", function (e) {
  e.preventDefault();
  submitForm();
});
