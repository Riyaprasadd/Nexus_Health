import { useState } from "react";
import { useSearchParams } from "react-router-dom";

export default function ResetPasswordConfirm() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token");

  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://127.0.0.1:8000/reset-password/confirm", {
        method: "POST",
        body: new URLSearchParams({
          token: token,
          new_password: newPassword,
        }),
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
      });

      const data = await res.json();
      if (res.ok) {
        setMessage("✅ Password reset successful! You can now log in.");
      } else {
        setMessage("❌ " + data.detail);
      }
    } catch (err) {
      setMessage("⚠️ Server error, try again later.");
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Reset Your Password</h2>
      {token ? (
        <form onSubmit={handleSubmit}>
          <input
            type="password"
            placeholder="Enter new password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
          <button type="submit">Reset Password</button>
        </form>
      ) : (
        <p>❌ Invalid or missing token</p>
      )}
      {message && <p>{message}</p>}
    </div>
  );
}
