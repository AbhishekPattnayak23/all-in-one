const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const rateLimit = require('express-rate-limit');
const validator = require('validator');
const User = require('../models/User');
const { sanitizeInput } = require('../middleware/sanitizer');
const router = express.Router();

// Rate limiting for login attempts
const loginLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 5, // limit each IP to 5 requests per windowMs
  message: { error: 'Too many login attempts, please try again later' },
  standardHeaders: true,
  legacyHeaders: false
});

// Secure login endpoint
router.post('/login', loginLimiter, sanitizeInput, async (req, res) => {
  try {
    const { username, password } = req.body;

    // Input validation
    if (!username || !password) {
      return res.status(400).json({ 
        error: 'Username and password are required' 
      });
    }

    // Sanitize and validate username
    const sanitizedUsername = validator.escape(username.trim());
    if (!validator.isAlphanumeric(sanitizedUsername)) {
      return res.status(400).json({ 
        error: 'Invalid username format' 
      });
    }

    // Find user (case-insensitive)
    const user = await User.findOne({ 
      username: { $regex: new RegExp(`^${sanitizedUsername}$`, 'i') } 
    });
    
    if (!user) {
      // Generic error message to prevent user enumeration
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }

    // Verify password
    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      // Log failed login attempt
      await User.findByIdAndUpdate(user._id, { 
        $push: { 
          failedLoginAttempts: { 
            ip: req.ip, 
            timestamp: new Date() 
          } 
        } 
      });
      
      return res.status(401).json({ 
        error: 'Invalid credentials' 
      });
    }

    // Generate secure JWT with short expiration
    const token = jwt.sign(
      { 
        userId: user._id, 
        username: user.username 
      }, 
      process.env.JWT_SECRET, 
      { 
        expiresIn: '1h',
        issuer: 'secure-app',
        audience: 'secure-app-users'
      }
    );

    // Clear any previous failed attempts
    await User.findByIdAndUpdate(user._id, { 
      $set: { failedLoginAttempts: [] } 
    });

    // Set secure cookie
    res.cookie('authToken', token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'strict',
      maxAge: 3600000 // 1 hour
    });

    res.json({ 
      success: true, 
      redirectUrl: '/dashboard' 
    });

  } catch (error) {
    console.error('Login error:', error.message);
    res.status(500).json({ 
      error: 'An error occurred during login' 
    });
  }
});

module.exports = router;
