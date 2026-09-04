export default function Card({ children }) {
    return (
        <div className="border border-gray-300 rounded-md px-4 py-2 shadow-md">
            {children}
        </div>
    )
}