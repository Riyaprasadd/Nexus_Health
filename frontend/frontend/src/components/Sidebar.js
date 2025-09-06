import React from "react";
import { NavLink } from "react-router-dom";
import { useTranslation } from "react-i18next";

function Sidebar() {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div className="p-4 bg-gray-900 text-white h-screen flex flex-col justify-between">
      {/* Menu */}
      <div>
        <h3 className="text-lg font-bold mb-4">Menu</h3>
        <ul className="space-y-3">
          <li>
            <NavLink
              to="/"
              className={({ isActive }) =>
                `cursor-pointer hover:text-blue-400 ${isActive ? "text-blue-400 font-semibold" : ""}`
              }
            >
              {t("login")}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/register"
              className={({ isActive }) =>
                `cursor-pointer hover:text-blue-400 ${isActive ? "text-blue-400 font-semibold" : ""}`
              }
            >
              {t("register")}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/chatbot"
              className={({ isActive }) =>
                `cursor-pointer hover:text-blue-400 ${isActive ? "text-blue-400 font-semibold" : ""}`
              }
            >
              {t("chatbot")}
            </NavLink>
          </li>
          <li>
            <NavLink
              to="/reset-password"
              className={({ isActive }) =>
                `cursor-pointer hover:text-blue-400 ${isActive ? "text-blue-400 font-semibold" : ""}`
              }
            >
              {t("resetPassword")}
            </NavLink>
          </li>
        </ul>
      </div>

      {/* Language Selector */}
      <div className="mt-6">
        <label className="block mb-2 text-sm">{t("language")}</label>
        <select
          onChange={(e) => changeLanguage(e.target.value)}
          defaultValue={i18n.language || "en"}
          className="w-full p-2 rounded bg-gray-800 text-white border border-gray-700"
        >
          <option value="en">English</option>
          <option value="hi">हिंदी</option>
          <option value="es">Español</option>
          <option value="fr">Français</option>
        </select>
      </div>
    </div>
  );
}

export default Sidebar;
