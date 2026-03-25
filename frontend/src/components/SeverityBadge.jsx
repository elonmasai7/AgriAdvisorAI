export default function SeverityBadge({ severity, score }) {
  const normalized = (severity || "").toLowerCase();
  const colorClass =
    normalized === "mild"
      ? "bg-green-100 text-green-800"
      : normalized === "moderate"
        ? "bg-yellow-100 text-yellow-800"
        : normalized === "severe"
          ? "bg-red-100 text-red-800"
          : "bg-gray-100 text-gray-800";

  return (
    <span className={`inline-flex rounded-full px-3 py-1 text-sm font-semibold ${colorClass}`}>
      {severity} ({score}/10)
    </span>
  );
}
