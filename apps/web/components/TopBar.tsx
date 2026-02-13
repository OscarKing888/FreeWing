"use client";

import Link from "next/link";

export function TopBar() {
  return (
    <div className="sticky top-0 z-20 border-b border-zinc-800 bg-zinc-950/80 backdrop-blur">
      <div className="mx-auto flex max-w-7xl items-center gap-4 px-4 py-3">
        <Link href="/" className="text-lg font-semibold tracking-tight">
          FreeWing
        </Link>
        <div className="flex-1">
          <input
            className="w-full rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm outline-none focus:border-zinc-600"
            placeholder="Search species / tag / place..."
          />
        </div>
        <Link href="/login" className="text-sm text-zinc-300 hover:text-white">
          Login
        </Link>
      </div>
    </div>
  );
}
