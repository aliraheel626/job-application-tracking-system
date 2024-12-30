import React from "react";
import "bootstrap/dist/css/bootstrap.min.css";

const STATUS_CHOICES = [
  { value: "applied", label: "Applied" },
  { value: "interview", label: "Interview Scheduled" },
  { value: "offer", label: "Offer Received" },
  { value: "rejected", label: "Rejected" },
  { value: "withdrawn", label: "Withdrawn" },
];

function Application({ application, onDelete, onUpdate }) {
  console.log(application);
  const formattedDate = new Date(application.application_date).toLocaleString(
    "en-US"
  );

  const handleStatusChange = (e) => {
    onUpdate(application.id, { ...application, status: e.target.value });
  };

  return (
    <div className="card mb-3">
      <div className="card-body">
        <h5 className="card-title">{application.company_name}</h5>
        <h6 className="card-subtitle mb-2 text-muted">
          {application.job_title}
        </h6>
        <div className="mb-3">
          <label htmlFor="status-select" className="form-label">
            Status:
          </label>
          <select
            id="status-select"
            className="form-select"
            value={application.status}
            onChange={handleStatusChange}
          >
            {STATUS_CHOICES.map((choice) => (
              <option key={choice.value} value={choice.value}>
                {choice.label}
              </option>
            ))}
          </select>
        </div>
        <p className="card-text">
          <small className="text-muted">Applied on: {formattedDate}</small>
        </p>
        {application.cv && (
          <a href={application.cv} className="btn btn-primary me-2" download>
            download cv
          </a>
        )}
        <button
          className="btn btn-danger"
          onClick={() => onDelete(application.id)}
        >
          Delete
        </button>
      </div>
    </div>
  );
}

export default Application;
