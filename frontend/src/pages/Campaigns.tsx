import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../lib/api";

export default function Campaigns() {
  const qc = useQueryClient();
  const { data } = useQuery({ queryKey: ["campaigns"], queryFn: async () => (await api.get("/campaigns")).data });
  const [form, setForm] = useState({ title: "", description: "", start_date: "", end_date: "", target_units: 0, is_public: true });
  const create = useMutation({
    mutationFn: async () => (await api.post("/campaigns", form)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["campaigns"] }),
  });

  return (
    <div>
      <h1>Campaigns</h1>
      <div className="panel">
        <div className="form-grid">
          <input placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
          <input placeholder="Description" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} />
          <input type="date" value={form.start_date} onChange={(e) => setForm({ ...form, start_date: e.target.value })} />
          <input type="date" value={form.end_date} onChange={(e) => setForm({ ...form, end_date: e.target.value })} />
          <input type="number" placeholder="Target units" value={form.target_units} onChange={(e) => setForm({ ...form, target_units: Number(e.target.value) })} />
        </div>
        <button onClick={() => create.mutate()}>Create campaign</button>
      </div>
      <ul className="list">
        {Array.isArray(data) &&
          data.map((c: any) => (
            <li key={c.id}>
              <strong>{c.title}</strong> — {c.status} ({c.start_date} to {c.end_date})
            </li>
          ))}
      </ul>
    </div>
  );
}
