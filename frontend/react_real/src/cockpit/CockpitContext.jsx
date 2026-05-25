import React, {
    createContext,
    useContext,
    useEffect,
    useMemo,
    useState
} from "react";

import { cockpitWidgets } from "./widgets";

const CockpitContext = createContext();

export function CockpitProvider({ children }) {

    const [widgets, setWidgets] = useState([]);

    useEffect(() => {

        const saved = localStorage.getItem(
            "comptapilot_widgets"
        );

        if (saved) {

            setWidgets(JSON.parse(saved));

        } else {

            setWidgets(cockpitWidgets);
        }

    }, []);

    useEffect(() => {

        if (widgets.length > 0) {

            localStorage.setItem(
                "comptapilot_widgets",
                JSON.stringify(widgets)
            );
        }

    }, [widgets]);

    function toggleFavorite(id) {

        setWidgets((current) =>
            current.map((widget) => {

                if (widget.id !== id) {
                    return widget;
                }

                return {
                    ...widget,
                    favorite: !widget.favorite
                };

            })
        );
    }

    const value = useMemo(() => ({
        widgets,
        toggleFavorite
    }), [widgets]);

    return (
        <CockpitContext.Provider value={value}>
            {children}
        </CockpitContext.Provider>
    );
}

export function useCockpit() {
    return useContext(CockpitContext);
}
