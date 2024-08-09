// document.addEventListener('DOMContentLoaded', function() {
//     const formElements = [
//       'country', 'hometown', 'placeOfBirth', 'address', 'gender', 'religion', 
//       'contactAddress', 'homeAddress', 'dateOfBirth', 'tribe', 'maritalStatus', 
//       'bloodGroup', 'genotype', 'disability'
//     ];

//     formElements.forEach(function(elementId) {
//       const inputField = document.getElementById(elementId);

//       // Load saved value from localStorage
//       const savedValue = localStorage.getItem(elementId);
//       if (savedValue) {
//         inputField.value = savedValue;
//       }

//       // Save value to localStorage on input change
//       inputField.addEventListener('input', function() {
//         localStorage.setItem(elementId, inputField.value);
//       });
//     });
//   });