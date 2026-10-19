
const form = document.getElementById("notification-form");
const channel = document.getElementById("channel");
const destination = document.getElementById("destination");
const message = document.getElementById("message");
const characterCount = document.getElementById("character-count");
const feedback = document.getElementById("feedback");

function updateDestinationField() {
  const isEmail = channel.value === "email";

  destination.type = isEmail ? "email" : "tel";
  destination.placeholder = isEmail
    ? "Enter email address"
    : "Enter phone number with country code";

  destination.maxLength = isEmail ? 254 : 16;
}

channel.addEventListener("change", updateDestinationField);

message.addEventListener("input", () => {
  characterCount.textContent = `${message.value.length} / 1000 characters`;
});

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const recipientName = document.getElementById("recipient-name").value.trim();
  const recipient = destination.value.trim();
  const notificationMessage = message.value.trim();

  if (!recipientName || !recipient || !notificationMessage) {
    feedback.textContent = "Please complete all fields.";
    return;
  }

  feedback.textContent =
    `Form validated locally for ${channel.value.toUpperCase()}. ` +
    "No notification has been sent yet.";
});

updateDestinationField();

