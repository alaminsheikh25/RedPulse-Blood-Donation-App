import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { api, type Appointment } from "../lib/api";

export default function Appointments() {
  const qc = useQueryClient();
  const { data } = useQuery<Appointment[]>({
    queryKey: ["appointments"],
    queryFn: async () => (await api.get("/appointments")).data,
  });

  const [form, setForm] = useState({ hospital_id: "", scheduled_at: "", duration_minutes: 30 });
  const create = useMutation({
    mutationFn: async () => (await api.post("/appointments", form)).data,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["appointments"] }),
  });

  return (
    <div>
      <h1>Appointments</h1>
      <div className="panel">
        <div className="form-grid">
          <input placeholder="Hospital ID" value={form.hospital_id} onChange={(e) => setForm({ ...form, hospital_id: e.target.value })} />
          <input type="datetime-local" value={form.scheduled_at} onChange={(e) => setForm({ ...form, scheduled_at: e.target.value })} />
          <input type="number" value={form.duration_minutes} onChange={(e) => setForm({ ...form, duration_minutes: Number(e.target.value) })} />
        </div>
        <button onClick={() => create.mutate()}>Book appointment</button>
      </div>
      <table className="table">
        <thead>
          <tr>
            <th>Hospital</th>
            <th>Scheduled</th>
            <th>Duration</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {data?.map((a) => (
            <tr key={a.id}>
              <td>{a.hospital_id}</td>
              <td>{new Date(a.scheduled_at).toLocaleString()}</td>
              <td>{a.duration_minutes} min</td>
              <td>{a.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
