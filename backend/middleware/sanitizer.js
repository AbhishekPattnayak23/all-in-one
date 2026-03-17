const xss = require('xss');
const DOMPurify = require('isomorphic-dompurify');

const sanitizeInput = (req, res, next) => {
  if (req.body && typeof req.body === 'object') {
    const sanitize = (obj) => {
      Object.keys(obj).forEach(key => {
        if (typeof obj[key] === 'string') {
          obj[key] = xss(DOMPurify.sanitize(obj[key]));
        } else if (typeof obj[key] === 'object' && obj[key] !== null) {
          sanitize(obj[key]);
        }
      });
    };
    sanitize(req.body);
  }
  next();
};

module.exports = { sanitizeInput };
