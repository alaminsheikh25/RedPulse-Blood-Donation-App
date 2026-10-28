import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api, type InventoryItem } from "../lib/api";

export default function Inventory() {
  const qc = useQueryClient();
  const { data } = useQuery<InventoryItem[]>({
    queryKey: ["inventory"],
    queryFn: async () => (await api.get("/inventory")).data,
  });

  const [form, setForm] = useState({ hospital_id: "", blood_group: "O+", units_available: 0 });
  const create = useMutation({
    mutationFn: async () => (await api.post("/inventory", form)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["inventory"] }),
  });

  return (
    <div>
      <h1>Inventory</h1>
      <div className="panel">
        <div className="form-grid">
          <input placeholder="Hospital ID" value={form.hospital_id} onChange={(e) => setForm({ ...form, hospital_id: e.target.value })} />
          <select value={form.blood_group} onChange={(e) => setForm({ ...form, blood_group: e.target.value })}>
            {["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].map((g) => (
              <option key={g}>{g}</option>
            ))}
          </select>
          <input type="number" placeholder="Units" value={form.units_available} onChange={(e) => setForm({ ...form, units_available: Number(e.target.value) })} />
        </div>
        <button onClick={() => create.mutate()}>Add stock</button>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>Hospital</th>
            <th>Blood group</th>
            <th>Available</th>
            <th>Reserved</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((i) => (
            <tr key={i.id}>
              <td>{i.hospital_id}</td>
              <td>{i.blood_group}</td>
              <td>{i.units_available}</td>
              <td>{i.units_reserved}</td>
              <td>{i.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
