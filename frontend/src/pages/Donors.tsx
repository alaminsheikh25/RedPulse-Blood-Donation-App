import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api } from "../lib/api";

export default function Donors() {
  const qc = useQueryClient();
  const [form, setForm] = useState({
    blood_group: "O+",
    date_of_birth: "1995-01-01",
    gender: "male",
    weight_kg: 60,
    hemoglobin_g_dl: 13.5,
    city: "",
  });

  const create = useMutation({
    mutationFn: async () => (await api.post("/donors", form)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["donors"] }),
  });

  return (
    <div>
      <h1>Donors</h1>
      <div className="panel">
        <h2>Register donor profile</h2>
        <div className="form-grid">
          <select value={form.blood_group} onChange={(e) => setForm({ ...form, blood_group: e.target.value })}>
            {["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].map((g) => (
              <option key={g}>{g}</option>
            ))}
          </select>
          <input type="date" value={form.date_of_birth} onChange={(e) => setForm({ ...form, date_of_birth: e.target.value })} />
          <select value={form.gender} onChange={(e) => setForm({ ...form, gender: e.target.value })}>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
          <input type="number" placeholder="Weight kg" value={form.weight_kg} onChange={(e) => setForm({ ...form, weight_kg: Number(e.target.value) })} />
          <input type="number" step="0.1" placeholder="Hemoglobin" value={form.hemoglobin_g_dl} onChange={(e) => setForm({ ...form, hemoglobin_g_dl: Number(e.target.value) })} />
          <input placeholder="City" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
        </div>
        <button onClick={() => create.mutate()}>Create profile</button>
      </div>
      <p className="muted">Donor list is managed via the API; use /donors/me to view your profile.</p>
    </div>
  );
}
