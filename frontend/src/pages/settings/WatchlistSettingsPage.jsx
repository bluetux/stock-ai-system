import React, { useEffect, useState } from "react";
import { Trash2, Plus, ListChecks } from "lucide-react";

const WatchlistSettingsPage = () => {
  const [watchlist, setWatchlist] = useState([]);
  const [groups, setGroups] = useState([]);
  const [selected, setSelected] = useState(null);
  const [editItem, setEditItem] = useState({});
  const [search, setSearch] = useState("");

  // 관심종목 + 그룹 불러오기
  useEffect(() => {
    fetch("/api/watchlist/")
      .then((res) => res.json())
      .then((data) => setWatchlist(data.watchlist || []));

    fetch("/api/groups/")
      .then((res) => res.json())
      .then((data) => {
        const flatGroups = [];
        for (const region in data) {
          for (const groupId in data[region]) {
            flatGroups.push({
              id: parseInt(groupId),
              name: data[region][groupId].name,
            });
          }
        }
        setGroups(flatGroups);
      });
  }, []);

  const handleSelect = (item) => {
    if (selected?.id === item.id) {
      setSelected(null);
    } else {
      setSelected(item);
      setEditItem({ ...item, group_ids: item.group_ids || [] });
    }
  };

  const handleInputChange = (field, value) => {
    setEditItem((prev) => ({ ...prev, [field]: value }));
  };

  const handleToggleGroup = (groupId) => {
    setEditItem((prev) => {
      const newGroupIds = prev.group_ids?.includes(groupId)
        ? prev.group_ids.filter((id) => id !== groupId)
        : [...(prev.group_ids || []), groupId];
      return { ...prev, group_ids: newGroupIds };
    });
  };

  const handleCancel = () => setSelected(null);

  const handleSave = () => {
    fetch("/api/watchlist/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(editItem),
    })
      .then((res) => {
        if (!res.ok) throw new Error("저장 실패");
        return res.json();
      })
      .then(() => {
        // 저장 후 새로고침
        return fetch("/api/watchlist/")
          .then((res) => res.json())
          .then((data) => {
            setWatchlist(data.watchlist || []);
            setSelected(null);
          });
      })
      .catch((err) => alert("저장 실패: " + err.message));
  };

  const handleDelete = (ticker) => {
    if (confirm(`${ticker} 종목을 삭제하시겠습니까?`)) {
      fetch(`/api/watchlist/${ticker}`, { method: "DELETE" }).then(() => {
        setWatchlist((prev) => prev.filter((item) => item.ticker !== ticker));
        setSelected(null);
      });
    }
  };

  const filteredList = watchlist
    .filter((item) => !item.ticker.startsWith("^")) // 지수 제외
    .filter(
      (item) =>
        item.alias.toLowerCase().includes(search.toLowerCase()) ||
        item.ticker.toLowerCase().includes(search.toLowerCase())
    );

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold flex items-center mb-2">
        <ListChecks className="w-5 h-5 mr-2" />
        관심종목 관리
      </h2>
      <p className="mb-4 text-gray-600">
        종목을 추가/수정/삭제하고 그룹도 연결할 수 있습니다.
      </p>

      {/* 상단: 검색 + 추가 */}
      <div className="flex items-center gap-4 mb-4">
        <input
          type="text"
          placeholder="검색 (Ticker, Alias)"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="border px-3 py-2 rounded w-64"
        />
        <button
          onClick={() => {
            setSelected({}); // 신규 추가 모드
            setEditItem({
              ticker: "",
              alias: "",
              region: "한국",
              is_active: true,
              icon: "",
              group_ids: [],
            });
          }}
          className="flex items-center px-3 py-2 bg-black text-white rounded hover:bg-gray-800"
        >
          <Plus className="w-4 h-4 mr-1" />
          종목 추가
        </button>
      </div>

      {/* ✅ 종목 추가 폼은 리스트 위에 위치 */}
      {selected && !selected.id && (
        <div className="p-4 mb-4 border bg-gray-50 rounded">
          <h3 className="text-lg font-semibold mb-4">신규 종목 추가</h3>
          <div className="grid grid-cols-1 gap-3">
            <div className="flex gap-4">
              <div className="flex-1">
                <label className="text-sm font-medium">주식코드</label>
                <input
                  value={editItem.ticker}
                  onChange={(e) =>
                    handleInputChange("ticker", e.target.value)
                  }
                  className="w-full border px-3 py-2 rounded mt-1"
                />
              </div>
              <div className="flex-1">
                <label className="text-sm font-medium">지역</label>
                <select
                  value={editItem.region}
                  onChange={(e) =>
                    handleInputChange("region", e.target.value)
                  }
                  className="w-full border px-3 py-2 rounded mt-1"
                >
                  <option>한국</option>
                  <option>미국</option>
                </select>
              </div>
              <div className="flex-1">
                <label className="text-sm font-medium">아이콘</label>
                <input
                  value={editItem.icon}
                  onChange={(e) =>
                    handleInputChange("icon", e.target.value)
                  }
                  className="w-full border px-3 py-2 rounded mt-1"
                />
              </div>
            </div>
            <div>
              <label className="text-sm font-medium">명칭</label>
              <input
                value={editItem.alias}
                onChange={(e) =>
                  handleInputChange("alias", e.target.value)
                }
                className="w-full border px-3 py-2 rounded mt-1"
              />
            </div>
            <div>
              <label className="text-sm font-medium">그룹</label>
              <div className="flex flex-wrap gap-2 mt-1">
                {groups.map((group) => (
                  <button
                    key={group.id}
                    type="button"
                    onClick={() => handleToggleGroup(group.id)}
                    className={`px-3 py-1 rounded-full text-sm border ${editItem.group_ids?.includes(group.id)
                      ? "bg-black text-white"
                      : "bg-white text-gray-600"
                      }`}
                  >
                    {group.name}
                  </button>
                ))}
              </div>
            </div>
            <div>
              <label className="text-sm font-medium">활성화</label>
              <div className="mt-2">
                <input
                  type="checkbox"
                  checked={editItem.is_active}
                  onChange={(e) =>
                    handleInputChange("is_active", e.target.checked)
                  }
                  className="w-5 h-5"
                />
                <span className="ml-2 text-sm">
                  {editItem.is_active ? "ON" : "OFF"}
                </span>
              </div>
            </div>
          </div>

          <div className="mt-4 flex justify-end gap-2">
            <button
              onClick={handleCancel}
              className="px-4 py-2 border rounded hover:bg-gray-100"
            >
              취소
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-black text-white rounded hover:bg-gray-800"
            >
              저장
            </button>
          </div>
        </div>
      )}

      {/* ✅ 종목 리스트 */}
      <div className="space-y-2">
        {filteredList.map((item) => (
          <div key={item.id}>
            <div
              className="p-3 bg-white border rounded cursor-pointer flex justify-between items-center hover:bg-gray-50"
              onClick={() => handleSelect(item)}
            >
              <div>
                <div className="font-semibold">{item.alias}</div>
                <div className="text-sm text-gray-500">
                  {item.ticker} / {item.region}
                </div>
              </div>
              <div className="text-green-600 font-semibold text-sm">
                {item.is_active ? "ON" : "OFF"}
              </div>
            </div>

            {/* 수정 폼 (기존 종목) */}
            {selected?.id === item.id && (
              <div className="p-4 mt-2 mb-4 border bg-gray-50 rounded">
                <h3 className="text-lg font-semibold mb-4">
                  {item.alias || "종목"} 정보 수정
                </h3>
                <div className="grid grid-cols-1 gap-3">
                  {/* ✅ 동일한 구조로 수정 입력 */}
                  <div className="flex gap-4">
                    <div className="flex-1">
                      <label className="text-sm font-medium">주식코드</label>
                      <input
                        value={editItem.ticker}
                        onChange={(e) =>
                          handleInputChange("ticker", e.target.value)
                        }
                        className="w-full border px-3 py-2 rounded mt-1"
                      />
                    </div>
                    <div className="flex-1">
                      <label className="text-sm font-medium">지역</label>
                      <select
                        value={editItem.region}
                        onChange={(e) =>
                          handleInputChange("region", e.target.value)
                        }
                        className="w-full border px-3 py-2 rounded mt-1"
                      >
                        <option>한국</option>
                        <option>미국</option>
                      </select>
                    </div>
                    <div className="flex-1">
                      <label className="text-sm font-medium">아이콘</label>
                      <input
                        value={editItem.icon}
                        onChange={(e) =>
                          handleInputChange("icon", e.target.value)
                        }
                        className="w-full border px-3 py-2 rounded mt-1"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="text-sm font-medium">명칭</label>
                    <input
                      value={editItem.alias}
                      onChange={(e) =>
                        handleInputChange("alias", e.target.value)
                      }
                      className="w-full border px-3 py-2 rounded mt-1"
                    />
                  </div>

                  <div>
                    <label className="text-sm font-medium">그룹</label>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {groups.map((group) => (
                        <button
                          key={group.id}
                          type="button"
                          onClick={() => handleToggleGroup(group.id)}
                          className={`px-3 py-1 rounded-full text-sm border ${editItem.group_ids?.includes(group.id)
                            ? "bg-black text-white"
                            : "bg-white text-gray-600"
                            }`}
                        >
                          {group.name}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="text-sm font-medium">활성화</label>
                    <div className="mt-2">
                      <input
                        type="checkbox"
                        checked={editItem.is_active}
                        onChange={(e) =>
                          handleInputChange("is_active", e.target.checked)
                        }
                        className="w-5 h-5"
                      />
                      <span className="ml-2 text-sm">
                        {editItem.is_active ? "ON" : "OFF"}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="mt-4 flex justify-between">
                  <button
                    onClick={() => handleDelete(editItem.ticker)}
                    className="px-4 py-2 text-white bg-red-500 rounded hover:bg-red-600"
                  >
                    삭제
                  </button>
                  <div className="space-x-2">
                    <button
                      onClick={handleCancel}
                      className="px-4 py-2 border rounded hover:bg-gray-100"
                    >
                      취소
                    </button>
                    <button
                      onClick={handleSave}
                      className="px-4 py-2 bg-black text-white rounded hover:bg-gray-800"
                    >
                      저장
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default WatchlistSettingsPage;