// pages/api/hello.js
export default function handler(req, res) {
    if (req.method === 'GET') {
      // Handle GET request
      res.status(200).json({ message: 'Hello from Next.js API!' });
    } 
    else if(req.method == 'POST'){
        const { start, dest } = req.body;
        console.log(start,dest);
        res.status(200).json({ message: 'Bye from Next.js API!' });
    }
    else {
      // Handle other HTTP methods
      res.setHeader('Allow', ['GET']);
      res.status(405).end(`Method ${req.method} Not Allowed`);
    }
  }
  