import './DeleteConfirmModal.css'

function DeleteConfirmModal({ isOpen, onClose, onConfirm, memberName, type = 'deactivate' }) {
  if (!isOpen) return null

  const isDeactivate = type === 'deactivate'
  const isDelete = type === 'delete'

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <h2>
          {isDeactivate && '⚠️ Inactivar Miembro'}
          {isDelete && '🗑️ Eliminar Miembro Permanentemente'}
        </h2>
        
        <p className="modal-message">
          {isDeactivate && (
            <>
              ¿Estás seguro de que deseas <strong>inactivar</strong> a <strong>{memberName}</strong>?
              <br /><br />
              El miembro quedará con estado inactivo pero se conservará en la base de datos.
              Podrás reactivarlo más adelante si lo deseas.
            </>
          )}
          {isDelete && (
            <>
              ¿Estás <strong>completamente seguro</strong> de que deseas <strong>eliminar permanentemente</strong> a <strong>{memberName}</strong>?
              <br /><br />
              <span className="warning-text">
                ⚠️ Esta acción NO se puede deshacer. Todos los datos del miembro se eliminarán permanentemente de la base de datos.
              </span>
            </>
          )}
        </p>

        <div className="modal-actions">
          <button onClick={onClose} className="btn-cancel">
            Cancelar
          </button>
          <button 
            onClick={onConfirm} 
            className={isDelete ? 'btn-delete' : 'btn-deactivate'}
          >
            {isDeactivate && 'Sí, Inactivar'}
            {isDelete && 'Sí, Eliminar Permanentemente'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default DeleteConfirmModal

