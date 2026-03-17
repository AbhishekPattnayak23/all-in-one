const mongoose = require('mongoose');
const bcrypt = require('bcrypt');

const userSchema = new mongoose.Schema({
  username: {
    type: String,
    required: true,
    unique: true,
    trim: true,
    minlength: 3,
    maxlength: 30,
    match: /^[a-zA-Z0-9_]+$/
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true,
    validate: {
      validator: function(v) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v);
      },
      message: 'Invalid email format'
    }
  },
  password: {
    type: String,
    required: true,
    minlength: 8
  },
  failedLoginAttempts: [{
    ip: String,
    timestamp: { type: Date, default: Date.now }
  }],
  lockUntil: Date,
  loginAttempts: { type: Number, default: 0 }
}, {
  timestamps: true
});

// Pre-save middleware to hash password
userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  
  try {
    const saltRounds = 12;
    this.password = await bcrypt.hash(this.password, saltRounds);
    next();
  } catch (error) {
    next(error);
  }
});

// Prevent password from being returned in queries
userSchema.methods.toJSON = function() {
  const user = this.toObject();
  delete user.password;
  delete user.failedLoginAttempts;
  delete user.lockUntil;
  delete user.loginAttempts;
  return user;
};

module.exports = mongoose.model('User', userSchema);
