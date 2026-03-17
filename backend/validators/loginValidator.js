const validator = require('validator');

const validateLoginInput = (username, password) => {
  const errors = {};

  if (!username || validator.isEmpty(username.trim())) {
    errors.username = 'Username is required';
  } else if (!validator.isAlphanumeric(username.trim())) {
    errors.username = 'Username must contain only letters and numbers';
  } else if (username.trim().length < 3 || username.trim().length > 30) {
    errors.username = 'Username must be between 3 and 30 characters';
  }

  if (!password || validator.isEmpty(password)) {
    errors.password = 'Password is required';
  } else if (password.length < 8) {
    errors.password = 'Password must be at least 8 characters';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors
  };
};

module.exports = validateLoginInput;
