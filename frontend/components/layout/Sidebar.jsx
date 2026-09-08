import Link from 'next/link';

export default function Sidebar() {
    return (
        <nav>
            <ul>
                <li><Link href="/dashboard">Dashboard</Link></li>
                <li><Link href="/projetos">Projetos</Link></li>
                <li><Link href="/membros">Membros</Link></li>
                <li><Link href="/configuracoes">Configurações</Link></li>
            </ul>
        </nav>
    )
}