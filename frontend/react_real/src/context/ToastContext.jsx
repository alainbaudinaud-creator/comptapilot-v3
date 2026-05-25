import React, {
    createContext,
    useContext,
    useMemo,
    useState
} from "react";

const ToastContext = createContext();

export function ToastProvider({ children }) {

    const [toasts, setToasts] = useState([]);

    function removeToast(id) {

        setToasts((current) =>
            current.filter((toast) => toast.id !== id)
        );
    }

    function pushToast(message, type = "info") {

        const id = Date.now();

        setToasts((current) => [
            ...current,
            { id, message, type }
        ]);

        setTimeout(() => {
            removeToast(id);
        }, 3500);
    }

    const value = useMemo(() => ({
        pushToast
    }), []);

    return (
        <ToastContext.Provider value={value}>

            {children}

            <div className="toast-container">

                {toasts.map((toast) => (

                    <div
                        key={toast.id}
                        className={`toast toast-${toast.type}`}
                    >
                        {toast.message}
                    </div>

                ))}

            </div>

        </ToastContext.Provider>
    );
}

export function useToast() {
    return useContext(ToastContext);
}
