import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api, type BloodRequest } from "../lib/api";

export default function Requests() {
  const qc = useQueryClient();
  const { data } = useQuery<BloodRequest[]>({
    queryKey: ["requests"],
    queryFn: async () => (await api.get("/requests")).data,
  });

  const [form, setForm] = useState({
    blood_group: "O+",
    units_required: 1,
    urgency: "routine",
    patient_name: "",
    location_description: "",
  });

  const create = useMutation({
    mutationFn: async () => (await api.post("/requests", form)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["requests"] }),
  });

  const runMatch = useMutation({
    mutationFn: async (id: string) => (await api.post(`/matches/request/${id}/run`)).data,
  });

  return (
    <div>
      <h1>Blood Requests</h1>
      <div className="panel">
        <h2>New request</h2>
        <div className="form-grid">
          <select value={form.blood_group} onChange={(e) => setForm({ ...form, blood_group: e.target.value })}>
            {["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"].map((g) => (
              <option key={g}>{g}</option>
            ))}
          </select>
          <input type="number" min={1} value={form.units_required} onChange={(e) => setForm({ ...form, units_required: Number(e.target.value) })} />
          <select value={form.urgency} onChange={(e) => setForm({ ...form, urgency: e.target.value })}>
            <option value="routine">Routine</option>
            <option value="urgent">Urgent</option>
            <option value="critical">Critical</option>
            <option value="emergency">Emergency</option>
          </select>
          <input placeholder="Patient name" value={form.patient_name} onChange={(e) => setForm({ ...form, patient_name: e.target.value })} />
          <input placeholder="Location" value={form.location_description} onChange={(e) => setForm({ ...form, location_description: e.target.value })} />
        </div>
        <button onClick={() => create.mutate()}>Create request</button>
      </div>

      <table className="table">
        <thead>
          <tr>
            <th>Blood group</th>
            <th>Units</th>
            <th>Urgency</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((r) => (
            <tr key={r.id}>
              <td>{r.blood_group}</td>
              <td>{r.units_fulfilled}/{r.units_required}</td>
              <td>{r.urgency}</td>
              <td>{r.status}</td>
              <td>
                <button onClick={() => runMatch.mutate(r.id)}>Run matching</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
