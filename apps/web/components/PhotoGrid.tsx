"use client";

import { useEffect, useState } from "react";

import { apiGet } from "@/lib/api";

import { PhotoCard } from "./PhotoCard";

type Photo = {
  id: number;
  taken_at?: string | null;
  place_text?: string | null;
  species_name?: string | null;
  thumb_url: string;
  preview_url: string;
  is_starred?: boolean | null;
};

type ListResp = { items: Photo[]; next_cursor?: number | null };

export function PhotoGrid() {
  const [items, setItems] = useState<Photo[]>([]);
  const [cursor, setCursor] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);

  async function loadMore() {
    if (loading) return;
    setLoading(true);
    try {
      const qs = cursor ? `?cursor=${cursor}` : "";
      const res = await apiGet<ListResp>(`/api/photos${qs}`);
      setItems((prev) => [...prev, ...res.items]);
      setCursor(res.next_cursor ?? null);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadMore();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="mx-auto max-w-7xl px-4 py-6">
      <div className="columns-2 gap-4 md:columns-3 xl:columns-4">
        {items.map((p) => (
          <PhotoCard key={p.id} p={p} />
        ))}
      </div>

      <div className="mt-6 flex justify-center">
        <button
          onClick={loadMore}
          disabled={loading || cursor === null}
          className="rounded-xl border border-zinc-800 bg-zinc-900 px-4 py-2 text-sm text-zinc-200 hover:border-zinc-600 disabled:opacity-40"
        >
          {cursor === null ? "No more" : loading ? "Loading..." : "Load more"}
        </button>
      </div>
    </div>
  );
}
