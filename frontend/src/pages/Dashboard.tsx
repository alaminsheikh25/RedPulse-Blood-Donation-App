import { useQuery } from "@tanstack/react-query";
import { api, type Summary } from "../lib/api";

export default function Dashboard() {
  const { data, isLoading } = useQuery<Summary>({
    queryKey: ["summary"],
    queryFn: async () => (await api.get("/reports/summary")).data,
  });

  if (isLoading) return <div>Loading...</div>;

  const cards = [
    { label: "Total donors", value: data?.total_donors ?? 0 },
    { label: "Total requests", value: data?.total_requests ?? 0 },
    { label: "Total donations", value: data?.total_donations ?? 0 },
    { label: "Units available", value: data?.units_available ?? 0 },
  ];

  return (
    <div>
      <h1>Dashboard</h1>
      <div className="card-grid">
        {cards.map((c) => (
          <div key={c.label} className="card">
            <div className="card-value">{c.value}</div>
            <div className="card-label">{c.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
