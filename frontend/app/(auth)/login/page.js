import {useState} from 'react';

export default function LoginPage() {
    const [email, setEmail] = useState('');
    const [senha, setSenha] = useState('');
    const [erro, setErro] = useState('');

    return (
        <div>
            Login
        </div>
    )
}