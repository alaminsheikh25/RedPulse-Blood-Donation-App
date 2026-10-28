import { useQuery } from "@tanstack/react-query";
import { api, type Summary } from "../lib/api";

export default function Reports() {
  const { data } = useQuery<Summary>({ queryKey: ["summary"], queryFn: async () => (await api.get("/reports/summary")).data });

  return (
    <div>
      <h1>Reports</h1>
      <div className="panel">
        <pre>{JSON.stringify(data, null, 2)}</pre>
      </div>
    </div>
  );
}
