export default function FilterPanel({ onChange }) {
  return (
    <div className="flex gap-3 items-center">
      <input
        className="px-3 py-2 rounded bg-gray-800 text-white"
        placeholder="Min price"
        onChange={(e) => onChange && onChange({ minPrice: e.target.value })}
      />
      <input
        className="px-3 py-2 rounded bg-gray-800 text-white"
        placeholder="Max price"
        onChange={(e) => onChange && onChange({ maxPrice: e.target.value })}
      />
    </div>
  );
}
