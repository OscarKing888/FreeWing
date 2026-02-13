import Image from "next/image";

import { API_BASE } from "@/lib/api";

type Photo = {
  id: number;
  taken_at?: string | null;
  place_text?: string | null;
  species_name?: string | null;
  thumb_url: string;
  preview_url: string;
  is_starred?: boolean | null;
};

export function PhotoCard({ p }: { p: Photo }) {
  const thumbSrc = `${API_BASE}${p.thumb_url}`;
  return (
    <div className="mb-4 break-inside-avoid overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-900/40 shadow-sm">
      <div className="relative">
        <Image
          src={thumbSrc}
          alt={p.species_name ?? `photo-${p.id}`}
          width={800}
          height={800}
          className="h-auto w-full object-cover"
          unoptimized
        />
        <div className="absolute right-3 top-3 rounded-full bg-zinc-950/70 px-2 py-1 text-xs text-zinc-200">
          {p.is_starred ? "★" : "☆"}
        </div>
      </div>
      <div className="px-3 py-3">
        <div className="text-sm font-medium text-zinc-100">
          {p.species_name ?? "Unknown Bird"}
        </div>
        <div className="mt-1 text-xs text-zinc-400">
          {p.place_text ?? "—"} · {p.taken_at ? p.taken_at.slice(0, 10) : "—"}
        </div>
      </div>
    </div>
  );
}
