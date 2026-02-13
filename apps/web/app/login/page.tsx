"use client";

import { useState } from "react";

import { apiPost } from "@/lib/api";

export default function LoginPage() {
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState<string | null>(null);

  async function onLogin() {
    setMsg(null);
    try {
      await apiPost("/api/auth/login", { username, password });
      window.location.href = "/";
    } catch (e: any) {
      setMsg(e?.message ?? "Login failed");
    }
  }

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100">
      <div className="mx-auto max-w-md px-4 py-16">
        <div className="rounded-2xl border border-zinc-800 bg-zinc-900/40 p-6">
          <div className="text-xl font-semibold">Login</div>
          <div className="mt-4 space-y-3">
            <input
              className="w-full rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-2"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="username"
            />
            <input
              className="w-full rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-2"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="password"
              type="password"
            />
            <button
              onClick={onLogin}
              className="w-full rounded-xl bg-white px-4 py-2 text-sm font-semibold text-zinc-950"
            >
              Sign in
            </button>
            {msg && <div className="text-sm text-red-400">{msg}</div>}
          </div>
        </div>
      </div>
    </div>
  );
}
