import { useState, useEffect } from "react";
import api from "../api";
import Application from "../components/Application";
import "../styles/Home.css";
import { useNavigate } from "react-router-dom";
import { Form, Button } from "react-bootstrap";
const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Add any logout logic here (e.g., clearing tokens, state)
    navigate("/logout"); // Navigate to the logout page
  };

  return (
    <button onClick={handleLogout} className="logout-button">
      Logout
    </button>
  );
};
const STATUS_CHOICES = [
  { value: "applied", label: "Applied" },
  { value: "interview", label: "Interview Scheduled" },
  { value: "offer", label: "Offer Received" },
  { value: "rejected", label: "Rejected" },
  { value: "withdrawn", label: "Withdrawn" },
];
function Home() {
  const [notes, setNotes] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [jobTitle, setJobTitle] = useState("");
  const [applicationDate, setApplicationDate] = useState("");
  const [status, setStatus] = useState(STATUS_CHOICES[0].value);
  const [cv, setCv] = useState(null);

  useEffect(() => {
    getNotes();
    console.log("Notes fetched");
    console.log("Notes:", notes);
  }, []);

  const getNotes = () => {
    api
      .get("/api/applications/")
      .then((res) => {
        setNotes(res.data);
      })
      .catch((e) => {
        alert(e);
        console.log(e);
      });
  };
  const deleteNote = (id) => {
    api
      .delete(`/api/applications/${id}/`)
      .then((res) => {
        if (res.status == 204) console.log("Note deleted successfully");
        else alert("Failed to delete note");
        getNotes();
      })
      .catch((e) => {
        alert(e);
      });
  };
  const updateApplication = (id, application) => {
    api
      .put(`/api/applications/${id}/`, application)
      .then((res) => {
        if (res.status === 200) {
          console.log("Application updated successfully");
          getNotes(); // Refresh the notes after a successful update
        } else {
          alert("Failed to update application");
        }
      })
      .catch((e) => {
        console.error("Error updating application:", e.response || e);
        alert("An error occurred while updating the application");
      });
  };
  const handleSubmit = (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("company_name", companyName);
    formData.append("job_title", jobTitle);
    formData.append("application_date", applicationDate);
    formData.append("status", status);

    // Append the file if it exists
    if (cv) {
      formData.append("cv", cv);
      console.log(cv);
    }

    api
      .post("/api/applications/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((res) => {
        if (res.status === 201) {
          console.log("Application created successfully");
        } else {
          alert("Failed to create application");
        }

        getNotes(); // Refresh the notes list
      })
      .catch((e) => {
        console.error("Error creating application:", e.response || e);
        alert("Error creating application");
      });
  };
  return (
    <div>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "20px",
          padding: "10px",
        }}
      >
        <h2 style={{ margin: "0" }}>Tasks</h2>
        <LogoutButton />
      </div>
      {/* {notes.map((note) => {
        console.log(note);
      })} */}
      {notes.map((note) => {
        console.log(note);
        return (
          <Application
            application={note}
            onDelete={deleteNote}
            onUpdate={updateApplication}
            key={note.id}
          />
        );
      })}
      <Form onSubmit={handleSubmit} className="p-3">
        {/* <Form.Group className="mb-3" controlId="formUser">
          <Form.Label>User</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter user"
            value={user}
            onChange={(e) => setUser(e.target.value)}
            required
          />
        </Form.Group> */}

        <Form.Group className="mb-3" controlId="formCompanyName">
          <Form.Label>Company Name</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter company name"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formJobTitle">
          <Form.Label>Job Title</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter job title"
            value={jobTitle}
            onChange={(e) => setJobTitle(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formApplicationDate">
          <Form.Label>Application Date</Form.Label>
          <Form.Control
            type="date"
            value={applicationDate}
            onChange={(e) => setApplicationDate(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formStatus">
          <Form.Label>Status</Form.Label>
          <Form.Select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
            required
          >
            {STATUS_CHOICES.map((choice) => (
              <option key={choice.value} value={choice.value}>
                {choice.label}
              </option>
            ))}
          </Form.Select>
        </Form.Group>
        <Form.Group className="mb-3" controlId="formPdf">
          <Form.Label>Attach PDF (Optional)</Form.Label>
          <Form.Control
            type="file"
            accept="application/pdf"
            onChange={(e) => setCv(e.target.files[0])}
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          Submit
        </Button>
      </Form>
    </div>
  );
}
export default Home;
