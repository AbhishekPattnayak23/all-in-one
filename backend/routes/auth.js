const express = require('express');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const router = express.Router();

// Import the user model - using cononical pattern from spec
// Assumed to return { id, username, email, password_hash } or null
let getUserByUsername;
try {
    const { getUserByUsername: imported } = require('../models/user');
    getUserByUsername = imported;
} catch (e) {
    // Stub for when User model is not yet available
    getUserByUsername = () => Promise.resolve(null);
}

/**
 * POST /api/auth/login
 * Authenticates user credentials and issues JWT token
 */
router.post('/login', async (req, res) => {
    const { username, password } = req.body;

    // Validate required fields
    if (!username || !password) {
        return res.status(400).json({
            detail: "Username and password are required.",
            error_code: "LOGIN_MISSING_FIELDS"
        });
    }

    try {
        // Retrieve user from database
        const user = await getUserByUsername(username);
        
        // User not found
        if (!user) {
            return res.status(400).json({
                detail: "Invalid credentials",
                error_code: "LOGIN_WRONG_CREDENTIALS"
            });
        }

        // Validate password
        const isMatch = await bcrypt.compare(password, user.password_hash);
        if (!isMatch) {
            return res.status(400).json({
                detail: "Invalid credentials",
                error_code: "LOGIN_WRONG_CREDENTIALS"
            });
        }

        // Generate JWT token
        const payload = {
            user_id: user.id,
            username: user.username,
            email: user.email
        };

        const token = jwt.sign(
            payload,
            process.env.JWT_SECRET || 'fallback-secret-change-me',
            { expiresIn: '7d', algorithm: 'HS256' }
        );

        // Successful response
        res.status(200).json({
            token,
            user: {
                id: user.id,
                username: user.username,
                email: user.email
            }
        });

    } catch (error) {
        // Internal server error
        res.status(500).json({
            detail: "Internal server error",
            error_code: "LOGIN_INTERNAL_ERROR"
        });
    }
});

module.exports = router;
