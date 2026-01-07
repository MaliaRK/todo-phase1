// pages/api/{{apiName}}.js
import { NextApiRequest, NextApiResponse } from 'next';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  // Input validation
  if (req.method !== '{{method}}') {
    return res.status(405).json({
      message: 'Method not allowed'
    });
  }

  try {
    // Process request based on method
    if (req.method === 'GET') {
      // Handle GET request
      return res.status(200).json({
        message: 'Success'
      });
    } else if (req.method === 'POST') {
      // Handle POST request
      // Validate req.body
      const { /* expected fields */ } = req.body;

      // Process data
      return res.status(200).json({
        message: 'Success'
      });
    }
    // Add other methods as needed
  } catch (error) {
    console.error('API Error:', error);
    return res.status(500).json({
      message: 'Internal server error'
    });
  }
}