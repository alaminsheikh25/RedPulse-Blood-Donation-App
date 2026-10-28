import { useQuery } from "@tanstack/react-query";
import { api } from "../lib/api";

export default function Notifications() {
  const { data } = useQuery({ queryKey: ["notifications"], queryFn: async () => (await api.get("/notifications")).data });

  return (
    <div>
      <h1>Notifications</h1>
      <ul className="list">
        {Array.isArray(data) &&
          data.map((n: any) => (
            <li key={n.id}>
              <strong>{n.title}</strong>
              <p>{n.body}</p>
              <span className="muted">{n.status}</span>
            </li>
          ))}
      </ul>
    </div>
  );
}
