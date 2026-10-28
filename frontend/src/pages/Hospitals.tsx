import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api, type Hospital } from "../lib/api";

export default function Hospitals() {
  const qc = useQueryClient();
  const { data } = useQuery<Hospital[]>({
    queryKey: ["hospitals"],
    queryFn: async () => (await api.get("/hospitals")).data,
  });

  const [form, setForm] = useState({ name: "", address: "", city: "", phone: "", has_blood_bank: false });
  const create = useMutation({
    mutationFn: async () => (await api.post("/hospitals", form)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["hospitals"] }),
  });

  return (
    <div>
      <h1>Hospitals</h1>
      <div className="panel">
        <div className="form-grid">
          <input placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <input placeholder="Address" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
          <input placeholder="City" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
          <input placeholder="Phone" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
          <label>
            <input type="checkbox" checked={form.has_blood_bank} onChange={(e) => setForm({ ...form, has_blood_bank: e.target.checked })} />
            Has blood bank
          </label>
        </div>
        <button onClick={() => create.mutate()}>Add hospital</button>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>Name</th>
            <th>City</th>
            <th>Blood bank</th>
            <th>Verified</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((h) => (
            <tr key={h.id}>
              <td>{h.name}</td>
              <td>{h.city}</td>
              <td>{h.has_blood_bank ? "Yes" : "No"}</td>
              <td>{h.is_verified ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
