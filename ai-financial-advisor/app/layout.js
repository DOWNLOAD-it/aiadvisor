// app/layout.js
import "bootstrap/dist/css/bootstrap.min.css"; // 1. Framework first
import "bootstrap-icons/font/bootstrap-icons.css"; // 2. Icons second
import "./globals.css"; // 3. Your custom styles last

export const metadata = {
  title: "AI Financial Advisor",
  description: "AI-powered financial insights",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
